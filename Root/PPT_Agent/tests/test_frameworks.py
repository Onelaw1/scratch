import os
import sys

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.engines.visual_engine import VisualEngine

def test_framework_generation():
    print("\nTesting Framework Generation...")
    
    engine = VisualEngine(output_dir="output/visuals_test")
    
    # 1. Test 3C Analysis
    print("Generating 3C Analysis...")
    path_3c = engine.generate_3c_analysis()
    assert os.path.exists(path_3c)
    print(f"3C Analysis created at: {path_3c}")
    
    # 2. Test Impact/Effort Matrix
    print("Generating Impact/Effort Matrix...")
    path_ie = engine.generate_impact_effort_matrix([])
    assert os.path.exists(path_ie)
    print(f"Impact/Effort Matrix created at: {path_ie}")
    
    # 3. Test RACI Matrix
    print("Generating RACI Matrix...")
    path_raci = engine.generate_raci_matrix()
    assert os.path.exists(path_raci)
    print(f"RACI Matrix created at: {path_raci}")
    
    print("\nAll Frameworks Generated Successfully!")

if __name__ == "__main__":
    test_framework_generation()
