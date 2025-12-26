"""
SVG conversion functions - extracted from original png_to_svg_converter.py
"""
import cv2
import numpy as np
from PIL import Image
import io
import base64


def png_to_svg_trace(image_array, threshold=128, simplify=2, invert=False, background_color=None):
    """
    Convert image to SVG using contour tracing
    
    Args:
        image_array: NumPy array of the image
        threshold: Threshold value for binary conversion (0-255)
        simplify: Simplification factor for contours
        invert: Whether to invert the binary threshold
        background_color: Optional background color for transparent images (hex string)
    
    Returns:
        tuple: (svg_content, num_contours)
    """
    # Handle alpha channel if present
    if image_array.shape[2] == 4 if len(image_array.shape) == 3 else False:
        image_array = _handle_alpha_channel(image_array, background_color)
    
    # Convert to grayscale if needed
    if len(image_array.shape) == 3:
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = image_array
    
    # Auto-detect if image should be inverted
    mean_val = gray.mean()
    if mean_val < 127 and not invert:
        invert = True
    
    # Apply threshold
    if invert:
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    else:
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get image dimensions
    height, width = binary.shape
    
    # Build SVG with multiple colors if original has colors
    svg_paths = []
    
    # Detect colors from original image
    if len(image_array.shape) == 3:
        for contour in contours:
            if len(contour) > simplify * 2:
                # Simplify contour
                epsilon = simplify
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Get average color inside contour
                mask = np.zeros(binary.shape, dtype=np.uint8)
                cv2.drawContours(mask, [contour], -1, 255, -1)
                mean_color = cv2.mean(image_array, mask=mask)[:3]
                
                # Build path data
                path_data = f"M {approx[0][0][0]} {approx[0][0][1]}"
                for point in approx[1:]:
                    path_data += f" L {point[0][0]} {point[0][1]}"
                path_data += " Z"
                
                # Convert color to hex
                color_hex = '#{:02x}{:02x}{:02x}'.format(
                    int(mean_color[0]), int(mean_color[1]), int(mean_color[2])
                )
                
                svg_paths.append((path_data, color_hex))
    else:
        for contour in contours:
            if len(contour) > simplify * 2:
                epsilon = simplify
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                path_data = f"M {approx[0][0][0]} {approx[0][0][1]}"
                for point in approx[1:]:
                    path_data += f" L {point[0][0]} {point[0][1]}"
                path_data += " Z"
                
                svg_paths.append((path_data, "#000000"))
    
    # Create SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
'''
    
    for path_data, color in svg_paths:
        svg += f'  <path d="{path_data}" fill="{color}" stroke="none"/>\n'
    
    svg += '</svg>'
    
    return svg, len(contours)


def png_to_svg_embed(image_array, preserve_alpha=True):
    """
    Embed image as base64 in SVG (not true vectorization)
    
    Args:
        image_array: NumPy array of the image
        preserve_alpha: Whether to preserve alpha channel
    
    Returns:
        str: SVG content with embedded image
    """
    # Convert to PIL Image
    pil_image = Image.fromarray(image_array)
    
    # Determine format based on alpha channel
    has_alpha = pil_image.mode in ('RGBA', 'LA', 'PA')
    img_format = "PNG" if (has_alpha and preserve_alpha) else "PNG"
    
    # Convert to base64
    buffered = io.BytesIO()
    pil_image.save(buffered, format=img_format)
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    height, width = image_array.shape[:2]
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <image width="{width}" height="{height}" xlink:href="data:image/png;base64,{img_base64}"/>
</svg>'''
    
    return svg


def _handle_alpha_channel(image_array, background_color=None):
    """
    Handle alpha channel in images
    
    Args:
        image_array: RGBA image array
        background_color: Background color to use (hex string or None for white)
    
    Returns:
        RGB image array
    """
    if background_color is None:
        background_color = "#FFFFFF"
    
    # Convert hex to RGB
    bg_color = tuple(int(background_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    # Create background
    background = np.ones((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8)
    background[:] = bg_color
    
    # Extract alpha channel
    alpha = image_array[:, :, 3] / 255.0
    
    # Blend with background
    for c in range(3):
        background[:, :, c] = (alpha * image_array[:, :, c] + (1 - alpha) * background[:, :, c]).astype(np.uint8)
    
    return background
