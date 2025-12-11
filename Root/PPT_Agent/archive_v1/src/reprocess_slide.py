import os
from pathlib import Path
from PIL import Image
from src.analysis.vision_agent import VisionAgent
import json
import fitz # PyMuPDF
import io

# Configuration
SLIDE_NUMBERS = [29, 44] # Slides identified as complex/problematic (1-based)
PDF_PATH = Path("data/input/2021_KOEM_2030전략수립_보고서_v2.1.pdf")
OUTPUT_DIR = Path("data/output/benchmark")

def reprocess_slides():
    agent = VisionAgent()
    
    if not PDF_PATH.exists():
        print(f"PDF not found: {PDF_PATH}")
        return

    print(f"Opening PDF: {PDF_PATH}")
    doc = fitz.open(PDF_PATH)
    
    # Zoom factor for high quality
    zoom = 300 / 72
    mat = fitz.Matrix(zoom, zoom)

    for slide_num in SLIDE_NUMBERS:
        idx = slide_num - 1
        if idx < 0 or idx >= len(doc):
            print(f"Slide {slide_num} out of range.")
            continue
            
        print(f"Processing Slide {slide_num}...")
        page = doc.load_page(idx)
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        
        try:
            result, usage = agent.analyze_slide(image, slide_number=slide_num)
            
            # Save new JSON
            output_path = OUTPUT_DIR / f"slide_{slide_num}.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)
            
            print(f"Saved updated JSON to {output_path}")
            
        except Exception as e:
            print(f"Error processing slide {slide_num}: {e}")
            
    doc.close()

if __name__ == "__main__":
    reprocess_slides()
