import sys
import os
import uuid
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from backend.main import app

client = TestClient(app)

def generate_uuid():
    return str(uuid.uuid4())

def verify_matrix_enhancements():
    print("Starting Matrix Enhancements Verification...")
    
    # Generate unique codes
    suffix = generate_uuid()[:8]
    group_code = f"JG_{suffix}"
    series_code = f"JS_{suffix}"
    pos_code = f"JP_{suffix}"
    
    # 1. Create Matrix Row with New Fields
    print("\n1. Creating Matrix Row with New Fields...")
    payload = [{
        "job_group_code": group_code,
        "job_group_name": "Test Group",
        "job_series_code": series_code,
        "job_series_name": "Test Series",
        "job_position_code": pos_code,
        "job_position_name": "Test Position",
        "current_grade": "5",
        "ideal_grade": "4",
        "min_years": 3,
        "max_years": 7
    }]
    
    response = client.post("/job-centric/classification/matrix", json=payload)
    if response.status_code != 200:
        print(f"   Failed to save matrix: {response.text}")
        return
    print("   Matrix row saved.")
    
    # 2. Verify Persistence
    print("\n2. Verifying Persistence...")
    response = client.get("/job-centric/classification/matrix")
    if response.status_code != 200:
        print(f"   Failed to retrieve matrix: {response.text}")
        return
        
    matrix = response.json()
    found = False
    for row in matrix:
        if row.get("job_position_code") == pos_code:
            found = True
            print(f"   Found row: {row}")
            
            # Check fields
            if row.get("current_grade") == "5":
                print("   SUCCESS: current_grade matches.")
            else:
                print(f"   FAILURE: current_grade mismatch. Expected '5', got '{row.get('current_grade')}'")
                
            if row.get("ideal_grade") == "4":
                print("   SUCCESS: ideal_grade matches.")
            else:
                print(f"   FAILURE: ideal_grade mismatch. Expected '4', got '{row.get('ideal_grade')}'")
                
            if row.get("min_years") == 3:
                print("   SUCCESS: min_years matches.")
            else:
                print(f"   FAILURE: min_years mismatch. Expected 3, got {row.get('min_years')}")
                
            if row.get("max_years") == 7:
                print("   SUCCESS: max_years matches.")
            else:
                print(f"   FAILURE: max_years mismatch. Expected 7, got {row.get('max_years')}")
            break
            
    if not found:
        print("   FAILURE: Row not found in matrix.")

if __name__ == "__main__":
    verify_matrix_enhancements()
