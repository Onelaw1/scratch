import os
import sys
import json
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.data_ingestion_service import DataIngestionService
from src.services.pptx_service import PPTXService
from src.models.schema import PresentationSchema, SlideContent

# Load env for API Key
load_dotenv()

def demo_image_ingestion():
    # Path to the uploaded image
    image_path = r"C:/Users/Administrator/.gemini/antigravity/brain/2b804d0d-f6e8-4044-969f-cc05ac9d87af/uploaded_image_1764831279865.png"
    
    print(f"Processing Image: {image_path}")
    
    if not os.path.exists(image_path):
        print("Error: Image file not found.")
        return

    # 1. Ingest Data (Image -> JSON)
    ingestion_service = DataIngestionService()
    print("Analyzing image with Gemini Vision...")
    data = ingestion_service.ingest_data(image_path, "image")
    
    print("\n--- Extracted Data (JSON) ---")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("-----------------------------\n")
    
    if not data:
        print("Failed to extract data.")
        return

    # 2. Generate PPT
    print("Generating PowerPoint...")
    pptx_service = PPTXService(output_dir="output/demo")
    
    # Create a generic schema based on extracted keys
    # We'll try to map it to a "Generic Analysis" slide
    slides = [
        SlideContent(
            title="Image Analysis Result", 
            bullet_points=[f"Analysis of uploaded slide image"]
        )
    ]
    schema = PresentationSchema(topic="Image Ingestion Demo", slides=slides)
    
    # Use a generic diagram type or just pass the data to see how it handles it
    # Since we don't know the exact keys yet, we'll use a "freeform" or "list" style if possible
    # For now, let's try to map it to a 'workflow' or just 'text' if keys are simple
    # But let's assume the AI returns something structured.
    
    # We will use the 'diagram_type' that best fits the keys, or default to 'swot' if it looks like 4 quadrants
    # For this specific image (Social Environment), it might return "Implications", "Causes", etc.
    # Let's force a simple "Key Findings" style if possible, or just use the raw data.
    
    design_schema = [
        {
            "diagram_type": "generic_text", # We might need to handle this in PPTXService or just use a known one
            # Let's use 'swot' as a fallback container if keys match, otherwise 'workflow'
            # Actually, let's just pass the data and let the diagram service try, 
            # or better, let's just dump it into a text slide for this demo if we can't determine type.
            # But wait, the user wants to see the "Agent" capability.
            # Let's use "smart_mapping" logic here simply.
            "diagram_data": data
        }
    ]
    
    # If keys look like SWOT, use SWOT.
    keys = [k.lower() for k in data.keys()]
    if any(k in keys for k in ['strengths', 'weaknesses']):
        design_schema[0]['diagram_type'] = 'swot'
    elif any(k in keys for k in ['product', 'price']):
        design_schema[0]['diagram_type'] = '4p'
    else:
        # Fallback: Use 'workflow' if steps, or just 'swot' container for generic lists
        design_schema[0]['diagram_type'] = 'swot' 

    output_file = pptx_service.create_presentation(schema, filename="demo_image_result.pptx", design_schema=design_schema)
    print(f"PPT Generated: {output_file}")

if __name__ == "__main__":
    demo_image_ingestion()
