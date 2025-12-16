import sys
import os
from fastapi.testclient import TestClient

# Add Root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from backend.main import app

client = TestClient(app)

def test_analysis_endpoints():
    print("Testing /job-analysis/analysis/fte-by-org...")
    print("\nTesting /job-analysis/analysis/fte-by-position...")
    response = client.get("/job-analysis/analysis/fte-by-position")
    if response.status_code == 200:
        print("[PASS] FTE by Position: OK")
        print(response.json())
    else:
        print(f"[FAIL] FTE by Position Failed: {response.status_code}")
        print(response.text)
    
    print("\nTesting /job-analysis/workload-entries/ (POST)...")
    payload = {
        "user_id": "user_test",
        "task_id": "task_1", 
        "volume": 240,
        "standard_time": 60
    }
    response = client.post("/job-analysis/workload-entries/", json=payload)
    if response.status_code == 200:
        print("[PASS] Save Entry: OK")
        print(response.json())
    else:
        print(f"[FAIL] Save Entry Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_analysis_endpoints()
