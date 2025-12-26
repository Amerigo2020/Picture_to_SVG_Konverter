"""
Image analysis functions to determine best conversion method
"""
import numpy as np
from PIL import Image


def analyze_image(image_array):
    """
    Analyze image characteristics
    
    Args:
        image_array: NumPy array of the image
    
    Returns:
        dict: Analysis results with keys:
            - has_alpha: bool
            - is_grayscale: bool
            - num_colors: int
            - complexity: str (low, medium, high)
            - is_photo: bool
    """
    analysis = {}
    
    # Check alpha channel
    if len(image_array.shape) == 3 and image_array.shape[2] == 4:
        analysis['has_alpha'] = True
        # Check if alpha is actually used
        alpha_channel = image_array[:, :, 3]
        analysis['has_transparency'] = np.any(alpha_channel < 255)
    else:
        analysis['has_alpha'] = False
        analysis['has_transparency'] = False
    
    # Check if grayscale
    if len(image_array.shape) == 2:
        analysis['is_grayscale'] = True
    elif len(image_array.shape) == 3:
        # Check if all channels are equal
        if image_array.shape[2] >= 3:
            r, g, b = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2]
            analysis['is_grayscale'] = np.array_equal(r, g) and np.array_equal(g, b)
        else:
            analysis['is_grayscale'] = False
    
    # Count unique colors (sample for performance)
    img_for_colors = image_array[:, :, :3] if len(image_array.shape) == 3 and image_array.shape[2] >= 3 else image_array
    
    # Sample image if too large
    h, w = img_for_colors.shape[:2]
    if h * w > 1000000:  # If more than 1M pixels, sample
        step = int(np.sqrt(h * w / 1000000))
        img_for_colors = img_for_colors[::step, ::step]
    
    # Reshape and count unique colors
    if len(img_for_colors.shape) == 3:
        pixels = img_for_colors.reshape(-1, img_for_colors.shape[2])
        unique_colors = len(np.unique(pixels, axis=0))
    else:
        unique_colors = len(np.unique(img_for_colors))
    
    analysis['num_colors'] = unique_colors
    
    # Determine complexity based on color count and variance
    variance = np.var(img_for_colors)
    
    if unique_colors < 10 and variance < 1000:
        analysis['complexity'] = 'low'
    elif unique_colors < 100 and variance < 5000:
        analysis['complexity'] = 'medium'
    else:
        analysis['complexity'] = 'high'
    
    # Detect if it's likely a photo (high color count + high variance)
    analysis['is_photo'] = unique_colors > 500 and variance > 3000
    
    # Image dimensions
    analysis['width'] = w
    analysis['height'] = h
    analysis['total_pixels'] = h * w
    
    return analysis


def recommend_method(analysis):
    """
    Recommend conversion method based on image analysis
    
    Args:
        analysis: dict from analyze_image()
    
    Returns:
        dict: Recommendation with keys:
            - method: str ('trace' or 'embed')
            - reason: str (explanation)
            - confidence: float (0-1)
    """
    recommendation = {
        'method': 'trace',
        'reason': '',
        'confidence': 0.5
    }
    
    reasons = []
    score = 0  # Positive = trace, Negative = embed
    
    # Check complexity
    if analysis['complexity'] == 'low':
        score += 3
        reasons.append("Geringe Komplexität -> ideal für Vektorisierung")
    elif analysis['complexity'] == 'medium':
        score += 1
        reasons.append("Mittlere Komplexität -> Vektorisierung möglich")
    else:
        score -= 2
        reasons.append("Hohe Komplexität -> Einbettung empfohlen")
    
    # Check if photo
    if analysis['is_photo']:
        score -= 3
        reasons.append("Foto-Eigenschaften erkannt -> Einbettung besser")
    
    # Check color count
    if analysis['num_colors'] < 20:
        score += 2
        reasons.append(f"Wenige Farben ({analysis['num_colors']}) -> gut für Vektoren")
    elif analysis['num_colors'] > 200:
        score -= 2
        reasons.append(f"Viele Farben ({analysis['num_colors']}) -> Einbettung besser")
    
    # Check transparency
    if analysis['has_transparency']:
        score += 1
        reasons.append("Transparenz vorhanden -> Vektorisierung kann diese nutzen")
    
    # Check size
    if analysis['total_pixels'] > 2000000:  # > 2MP
        score -= 1
        reasons.append("Großes Bild -> Einbettung eventuell effizienter")
    
    # Make decision
    if score > 2:
        recommendation['method'] = 'trace'
        recommendation['confidence'] = min(0.9, 0.5 + score * 0.1)
    elif score < -2:
        recommendation['method'] = 'embed'
        recommendation['confidence'] = min(0.9, 0.5 + abs(score) * 0.1)
    else:
        # Neutral - default to trace for smaller images, embed for larger
        if analysis['total_pixels'] < 1000000:
            recommendation['method'] = 'trace'
            reasons.append("Standardgröße -> Vektorisierung versuchen")
        else:
            recommendation['method'] = 'embed'
            reasons.append("Größeres Bild -> Einbettung sicherer")
        recommendation['confidence'] = 0.5
    
    recommendation['reason'] = " | ".join(reasons)
    
    return recommendation
