import sys
import os
from fastapi.testclient import TestClient
import json

# Add Job Management System root to path
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

from backend.main import app
from backend.database import Base, engine, SessionLocal
from backend import models

# Create tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_strategy_api():
    print("Starting Strategic Analysis API Test...")

    # 1. Create Institution
    inst_data = {
        "name": "Test Institution",
        "code": "TEST001",
        "category_type": "MARKET",
        "evaluation_group": "SOC"
    }
    response = client.post("/institutions/", json=inst_data)
    if response.status_code == 200:
        inst_id = response.json()["id"]
        print(f"Created Institution: {inst_id}")
    else:
        # Try to find existing
        response = client.get("/institutions/")
        insts = response.json()
        if insts:
            inst_id = insts[0]["id"]
            print(f"Using existing Institution: {inst_id}")
        else:
            print(f"Failed to create institution: {response.text}")
            return

    # 2. Create Strategic Analysis
    analysis_data = {
        "institution_id": inst_id,
        "analysis_type": "SWOT",
        "title": "Test SWOT Analysis",
        "content": json.dumps({"strengths": ["Good Team"], "weaknesses": ["Small Budget"]})
    }
    response = client.post("/api/strategy/", json=analysis_data)
    assert response.status_code == 200, f"Create failed: {response.text}"
    analysis_id = response.json()["id"]
    print(f"Created Analysis: {analysis_id}")

    # 3. Read Analysis
    response = client.get(f"/api/strategy/{analysis_id}")
    assert response.status_code == 200, f"Read failed: {response.text}"
    assert response.json()["title"] == "Test SWOT Analysis"
    print("Read Analysis: OK")

    # 4. Update Analysis
    update_data = {
        "title": "Updated SWOT Analysis"
    }
    response = client.put(f"/api/strategy/{analysis_id}", json=update_data)
    assert response.status_code == 200, f"Update failed: {response.text}"
    assert response.json()["title"] == "Updated SWOT Analysis"
    print("Update Analysis: OK")

    # 5. List by Institution
    response = client.get(f"/api/strategy/institution/{inst_id}")
    assert response.status_code == 200, f"List failed: {response.text}"
    assert len(response.json()) > 0
    print("List Analysis: OK")

    # 6. Delete Analysis
    response = client.delete(f"/api/strategy/{analysis_id}")
    assert response.status_code == 200, f"Delete failed: {response.text}"
    print("Delete Analysis: OK")

    # Verify Delete
    response = client.get(f"/api/strategy/{analysis_id}")
    assert response.status_code == 404
    print("Verify Delete: OK")

    print("All tests passed!")

if __name__ == "__main__":
    test_strategy_api()
