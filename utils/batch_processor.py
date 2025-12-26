"""
Batch processing for multiple images
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import io
import zipfile
from typing import List, Callable, Tuple
import numpy as np


def process_batch(
    images_data: List[Tuple[str, np.ndarray]],
    conversion_func: Callable,
    max_workers: int = 4,
    progress_callback: Callable = None,
    **conversion_kwargs
) -> List[Tuple[str, str, bool, str]]:
    """
    Process multiple images in parallel
    
    Args:
        images_data: List of (filename, image_array) tuples
        conversion_func: Function to call for each image
        max_workers: Maximum number of parallel workers
        progress_callback: Optional callback function(current, total)
        **conversion_kwargs: Additional arguments for conversion_func
    
    Returns:
        List of (filename, svg_content, success, error_message) tuples
    """
    results = []
    total = len(images_data)
    
    def process_single(filename, image_array):
        try:
            result = conversion_func(image_array, **conversion_kwargs)
            # Handle different return types
            if isinstance(result, tuple):
                svg_content = result[0]
            else:
                svg_content = result
            return (filename, svg_content, True, "")
        except Exception as e:
            return (filename, "", False, str(e))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_data = {
            executor.submit(process_single, filename, img): (filename, img)
            for filename, img in images_data
        }
        
        # Collect results as they complete
        completed = 0
        for future in as_completed(future_to_data):
            result = future.result()
            results.append(result)
            completed += 1
            
            if progress_callback:
                progress_callback(completed, total)
    
    # Sort results by original order
    filename_order = {fn: i for i, (fn, _) in enumerate(images_data)}
    results.sort(key=lambda x: filename_order.get(x[0], 999))
    
    return results


def create_zip_archive(svg_results: List[Tuple[str, str, bool, str]]) -> bytes:
    """
    Create a ZIP archive from SVG conversion results
    
    Args:
        svg_results: List of (filename, svg_content, success, error) tuples
    
    Returns:
        bytes: ZIP file content
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, svg_content, success, error in svg_results:
            if success:
                # Convert filename to .svg
                svg_filename = filename.rsplit('.', 1)[0] + '.svg'
                zip_file.writestr(svg_filename, svg_content)
            else:
                # Add error log for failed conversions
                error_filename = filename.rsplit('.', 1)[0] + '_ERROR.txt'
                zip_file.writestr(error_filename, f"Conversion failed: {error}")
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()
