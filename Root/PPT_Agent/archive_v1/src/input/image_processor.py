from PIL import Image
import numpy as np

class ImagePreprocessor:
    """
    Prepares images for Vision AI analysis.
    """
    
    @staticmethod
    def normalize_image(image: Image.Image, max_dimension: int = 2048) -> Image.Image:
        """
        Resizes image if it exceeds max_dimension while maintaining aspect ratio.
        Vision APIs often have size limits or process smaller images faster.
        
        Args:
            image (Image.Image): Input PIL Image.
            max_dimension (int): Maximum width or height.
            
        Returns:
            Image.Image: Processed image.
        """
        width, height = image.size
        if max(width, height) <= max_dimension:
            return image
            
        scale = max_dimension / max(width, height)
        new_size = (int(width * scale), int(height * scale))
        
        return image.resize(new_size, Image.Resampling.LANCZOS)

    @staticmethod
    def to_base64(image: Image.Image) -> str:
        """
        Helper to convert PIL Image to base64 string if needed for API calls.
        """
        import base64
        import io
        
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
