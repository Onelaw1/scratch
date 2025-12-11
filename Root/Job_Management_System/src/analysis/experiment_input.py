import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.input.pdf_loader import PDFLoader
from src.analysis.vision_agent import VisionAgent

load_dotenv()

INPUT_DIR = Path("data/input")
OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def test_image_method(pdf_path: Path, agent: VisionAgent):
    print(f"\n--- Testing Image Method for {pdf_path.name} ---")
    loader = PDFLoader(dpi=150) # Lower DPI for speed in test
    start_time = time.time()
    
    images = loader.convert_to_images(pdf_path)
    print(f"Converted to {len(images)} images in {time.time() - start_time:.2f}s")
    
    # Analyze first page only for comparison
    if images:
        img_start = time.time()
        result = agent.analyze_slide(images[0], slide_number=1)
        print(f"Analysis took {time.time() - img_start:.2f}s")
        return result, time.time() - start_time
    return None, 0

def test_native_method(pdf_path: Path, model_name: str = "gemini-1.5-pro"):
    print(f"\n--- Testing Native Method for {pdf_path.name} ---")
    start_time = time.time()
    
    # Upload file
    print("Uploading file to Gemini...")
    sample_file = genai.upload_file(path=pdf_path, display_name=pdf_path.name)
    print(f"Upload complete: {sample_file.uri}")
    
    # Wait for processing
    while sample_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(1)
        sample_file = genai.get_file(sample_file.name)
    
    if sample_file.state.name == "FAILED":
        print("File processing failed.")
        return None, 0

    print("File processed.")
    
    # Generate content
    model = genai.GenerativeModel(model_name)
    prompt = "Analyze the first slide of this PDF. Return the structure as a JSON object matching the schema: {title, content, layout_type}."
    
    gen_start = time.time()
    response = model.generate_content([sample_file, prompt])
    print(f"Generation took {time.time() - gen_start:.2f}s")
    
    # Cleanup
    genai.delete_file(sample_file.name)
    
    return response.text, time.time() - start_time

def main():
    pdfs = list(INPUT_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PDF files found in {INPUT_DIR}. Please add a PDF file.")
        return

    target_pdf = pdfs[0] # Pick the first one
    print(f"Target PDF: {target_pdf}")
    
    agent = VisionAgent()
    
    # 1. Image Method
    try:
        img_result, img_time = test_image_method(target_pdf, agent)
        print(f"Image Method Result: {img_result}")
        
        if img_result:
            output_json_path = OUTPUT_DIR / "slide_analysis.json"
            with open(output_json_path, "w", encoding="utf-8") as f:
                f.write(img_result.to_prompt_format())
            print(f"Saved analysis to {output_json_path}")

    except Exception as e:
        print(f"Image Method Failed: {e}")

    # 2. Native Method (Skipping for now to focus on Image Method integration)
    # try:
    #     native_result, native_time = test_native_method(target_pdf)
    #     print(f"Native Method Result: {native_result}")
    # except Exception as e:
    #     print(f"Native Method Failed: {e}")

if __name__ == "__main__":
    main()
