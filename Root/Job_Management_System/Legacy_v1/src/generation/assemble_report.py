import json
import re
from pathlib import Path
from pptx import Presentation
from src.generation.experiment_output import render_slide_to_pptx

BENCHMARK_DIR = Path("data/output/benchmark")
OUTPUT_PPTX = Path("data/output/full_reproduction.pptx")

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', str(s))]

def assemble_report():
    print("Assembling full report...")
    
    # 1. Find all slide JSONs
    json_files = list(BENCHMARK_DIR.glob("slide_*.json"))
    if not json_files:
        print("No slide JSONs found in benchmark directory.")
        return

    # 2. Sort by slide number (natural sort)
    json_files.sort(key=lambda p: natural_sort_key(p.name))
    
    print(f"Found {len(json_files)} slides.")

    # 3. Create Presentation
    prs = Presentation()
    
    # 4. Render each slide
    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            print(f"Rendering {json_file.name}...")
            render_slide_to_pptx(prs, data)
            
        except Exception as e:
            print(f"Error rendering {json_file.name}: {e}")

    # 5. Save
    import time
    timestamp = int(time.time())
    OUTPUT_PPTX = f"data/output/full_reproduction_{timestamp}.pptx"
    prs.save(OUTPUT_PPTX)
    print(f"Full report saved to: {OUTPUT_PPTX}")

if __name__ == "__main__":
    assemble_report()
