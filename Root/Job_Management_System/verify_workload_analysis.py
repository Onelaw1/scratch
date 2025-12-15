import sys
import os
from fastapi.testclient import TestClient

# Add Root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from backend.main import app

client = TestClient(app)

def test_analysis_endpoints():
    print("Testing /job-analysis/analysis/fte-by-org...")
    response = client.get("/job-analysis/analysis/fte-by-org")
    if response.status_code == 200:
        print("✅ FTE by Org: OK")
        print(response.json())
    else:
        print(f"❌ FTE by Org Failed: {response.status_code}")
        print(response.text)

    print("\nTesting /job-analysis/analysis/fte-by-position...")
    response = client.get("/job-analysis/analysis/fte-by-position")
    if response.status_code == 200:
        print("✅ FTE by Position: OK")
        print(response.json())
    else:
        print(f"❌ FTE by Position Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_analysis_endpoints()
