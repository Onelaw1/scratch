import time
import json
import csv
from pathlib import Path
from src.input.pdf_loader import PDFLoader
from src.analysis.vision_agent import VisionAgent
from src.generation.experiment_output import generate_html

# Configuration
INPUT_PDF = Path("data/input/2021_KOEM_2030전략수립_보고서_v2.1.pdf")
OUTPUT_DIR = Path("data/output/benchmark")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_FILE = OUTPUT_DIR / "benchmark_report.csv"

def run_benchmark():
    print(f"Starting benchmark for {INPUT_PDF}...")
    
    # 1. Load PDF
    loader = PDFLoader(dpi=150) # Lower DPI for speed/cost balance if needed, but 150 is decent
    start_load = time.time()
    images = loader.convert_to_images(INPUT_PDF)
    load_time = time.time() - start_load
    print(f"PDF loaded in {load_time:.2f}s. Total pages: {len(images)}")

    # Initialize Agent
    agent = VisionAgent()
    
    # Prepare Report CSV
    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Page", "Status", "Time(s)", "InputTokens", "OutputTokens", "TotalTokens", "EstCost($)"])
        
        total_input = 0
        total_output = 0
        total_time = 0
        
        # 2. Process Loop
        # LIMIT for testing: Process first 3 pages to verify, then user can ask for more. 
        # User asked for "Full", but let's do a safe batch first or just go for it?
        # The user said "Input report ALL". I will try to process all, but catch errors.
        # To avoid timeout, I'll process a subset first or print progress.
        # Let's process ALL as requested.
        
        results_data = []

        for i, img in enumerate(images):
            page_num = i + 1
            print(f"\n--- Processing Page {page_num} ---")
            
            page_start = time.time()
            try:
                # Analyze
                slide_data, usage = agent.analyze_slide(img, slide_number=page_num)
                
                # Generate Output (HTML for now)
                # We need to adapt generate_html to take a specific path or return string
                # For now, we just run it and it saves to 'data/output/test_slide.html'
                # We should probably save individual files.
                # Let's hack generate_html slightly or just rely on the side effect for now 
                # but ideally we save unique files.
                # For this benchmark, the generation cost is negligible compared to Vision.
                # We will just save the JSON.
                
                json_path = OUTPUT_DIR / f"slide_{page_num}.json"
                with open(json_path, "w", encoding="utf-8") as jf:
                    json.dump(slide_data.model_dump(), jf, ensure_ascii=False, indent=2)
                
                # Metrics
                p_time = time.time() - page_start
                in_tok = usage.get("prompt_token_count", 0)
                out_tok = usage.get("candidates_token_count", 0)
                tot_tok = usage.get("total_token_count", 0)
                
                # Cost Est (Gemini 1.5 Flash: $0.075/1M input, $0.30/1M output - approx)
                # Let's use generic pricing for estimation: Input $0.10/1M, Output $0.40/1M
                cost = (in_tok / 1_000_000 * 0.10) + (out_tok / 1_000_000 * 0.40)
                
                writer.writerow([page_num, "Success", f"{p_time:.2f}", in_tok, out_tok, tot_tok, f"{cost:.6f}"])
                
                total_input += in_tok
                total_output += out_tok
                total_time += p_time
                results_data.append(slide_data.model_dump())
                
            except Exception as e:
                print(f"Error on page {page_num}: {e}")
                writer.writerow([page_num, "Error", "0", "0", "0", "0", "0"])
        
        # Summary
        print("\n--- Benchmark Complete ---")
        print(f"Total Pages: {len(images)}")
        print(f"Total Time: {total_time:.2f}s")
        print(f"Total Tokens: {total_input + total_output} (In: {total_input}, Out: {total_output})")
        
        # Save full combined JSON
        with open(OUTPUT_DIR / "full_report.json", "w", encoding="utf-8") as f:
            json.dump({"slides": results_data}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_benchmark()
