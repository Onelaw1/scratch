import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Union
from PIL import Image
import io

class PDFLoader:
    """
    Handles loading of PDF files and converting them to images for analysis.
    """
    
    def __init__(self, dpi: int = 300):
        """
        Initialize the PDFLoader.
        
        Args:
            dpi (int): Dots per inch for rendering images. Higher DPI = better OCR/Vision.
                       300 is recommended for high-quality text analysis.
        """
        self.dpi = dpi
        self.zoom = dpi / 72  # 72 is the default PDF point size

    def convert_to_images(self, pdf_path: Union[str, Path]) -> List[Image.Image]:
        """
        Convert all pages of a PDF to PIL Images.
        
        Args:
            pdf_path (str | Path): Path to the PDF file.
            
        Returns:
            List[Image.Image]: List of PIL Image objects, one per page.
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        doc = fitz.open(pdf_path)
        images = []
        
        # Matrix for zooming (scaling)
        mat = fitz.Matrix(self.zoom, self.zoom)
        
        print(f"Processing PDF: {pdf_path.name} ({len(doc)} pages)")
        
        for page_num, page in enumerate(doc):
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            images.append(img)
            print(f"  - Converted page {page_num + 1}/{len(doc)}")
            
        doc.close()
        return images

if __name__ == "__main__":
    # Test stub
    import sys
    if len(sys.argv) > 1:
        loader = PDFLoader()
        imgs = loader.convert_to_images(sys.argv[1])
        print(f"Successfully converted {len(imgs)} pages.")
