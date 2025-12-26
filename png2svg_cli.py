#!/usr/bin/env python3
"""
PNG to SVG Converter - Command Line Version
Convert images to SVG format from the command line
"""
import argparse
import cv2
import numpy as np
from PIL import Image
import base64
import io

def trace_to_svg(image_path, output_path, threshold=128, simplify=2, invert_auto=True):
    """Convert image to SVG using contour tracing"""
    # Load image
    img = Image.open(image_path)
    img_rgb = img.convert('RGB')
    image_array = np.array(img_rgb)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    
    # Auto-detect if image should be inverted
    if invert_auto:
        mean_val = gray.mean()
        invert = mean_val < 127
    else:
        invert = False
    
    # Apply threshold
    if invert:
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    else:
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get image dimensions
    height, width = gray.shape
    
    # Build SVG
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>
'''
    
    path_count = 0
    
    # Process contours
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if len(contour) > 3 and area > 50:
            # Simplify contour
            epsilon = simplify
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) > 2:
                # Get average color
                mask = np.zeros(gray.shape, dtype=np.uint8)
                cv2.drawContours(mask, [contour], -1, 255, -1)
                mean_color = cv2.mean(image_array, mask=mask)[:3]
                
                # Build path
                path_data = f"M {approx[0][0][0]} {approx[0][0][1]}"
                for point in approx[1:]:
                    path_data += f" L {point[0][0]} {point[0][1]}"
                path_data += " Z"
                
                # Color
                r, g, b = int(mean_color[0]), int(mean_color[1]), int(mean_color[2])
                color_hex = f'#{r:02x}{g:02x}{b:02x}'
                
                svg += f'  <path d="{path_data}" fill="{color_hex}"/>\n'
                path_count += 1
    
    svg += '</svg>'
    
    # Save
    with open(output_path, 'w') as f:
        f.write(svg)
    
    return path_count, len(svg)

def embed_to_svg(image_path, output_path):
    """Embed image as base64 in SVG"""
    # Load image
    img = Image.open(image_path)
    img_rgb = img.convert('RGB')
    
    # Convert to base64
    buffered = io.BytesIO()
    img_rgb.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    width, height = img.size
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <image width="{width}" height="{height}" xlink:href="data:image/png;base64,{img_base64}"/>
</svg>'''
    
    # Save
    with open(output_path, 'w') as f:
        f.write(svg)
    
    return len(svg)

def main():
    parser = argparse.ArgumentParser(description='Convert PNG/images to SVG')
    parser.add_argument('input', help='Input image file')
    parser.add_argument('output', help='Output SVG file')
    parser.add_argument('-m', '--method', choices=['trace', 'embed'], default='trace',
                       help='Conversion method (default: trace)')
    parser.add_argument('-t', '--threshold', type=int, default=128,
                       help='Threshold for tracing (0-255, default: 128)')
    parser.add_argument('-s', '--simplify', type=int, default=2,
                       help='Simplification level (default: 2)')
    parser.add_argument('--no-auto-invert', action='store_true',
                       help='Disable automatic inversion detection')
    
    args = parser.parse_args()
    
    print(f"Converting {args.input} to {args.output}")
    print(f"Method: {args.method}")
    
    if args.method == 'trace':
        print(f"Threshold: {args.threshold}, Simplify: {args.simplify}")
        path_count, size = trace_to_svg(
            args.input, 
            args.output,
            threshold=args.threshold,
            simplify=args.simplify,
            invert_auto=not args.no_auto_invert
        )
        print(f"Created {path_count} paths")
        print(f"SVG size: {size / 1024:.2f} KB")
    else:
        size = embed_to_svg(args.input, args.output)
        print(f"SVG size: {size / 1024:.2f} KB")
    
    print(f"✓ Saved to {args.output}")

if __name__ == '__main__':
    main()
