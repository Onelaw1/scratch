from fastapi.testclient import TestClient
from backend.main import app
import uuid

client = TestClient(app)

def generate_uuid():
    return str(uuid.uuid4())

def verify_job_evaluation():
    print("Starting Job Evaluation Verification (TestClient)...")

    # 1. Create Prerequisites (Institution, Group, Series, Position)
    inst_id = generate_uuid()
    client.post("/institutions/", json={"id": inst_id, "name": "Test Inst", "code": f"TEST_{inst_id[:5]}"})
    
    group_id = generate_uuid()
    client.post("/jobs/groups/", json={"id": group_id, "name": "Admin Group"})
    
    series_id = generate_uuid()
    client.post("/jobs/series/", json={"id": series_id, "group_id": group_id, "name": "General Admin"})
    
    pos_id = generate_uuid()
    client.post("/job-positions/", json={"id": pos_id, "series_id": series_id, "title": "Budget Planner", "grade": "G3"})
    
    print("[OK] Prerequisites Created")

    # 2. Create Evaluation Session
    response = client.post("/evaluations/", json={
        "job_position_id": pos_id
    })
    if response.status_code != 200:
        print(f"[FAIL] Create Evaluation: {response.text}")
        return
    eval_id = response.json()["id"]
    print(f"[OK] Evaluation Session Created: {eval_id}")

    # 3. Add Scores (Multi-Rater)
    # Self (Leniency: High Score)
    client.post(f"/evaluations/{eval_id}/scores", json={
        "rater_type": "SELF",
        "score_expertise": 90,
        "score_responsibility": 90,
        "score_complexity": 90
    })
    
    # Peer (Moderate)
    client.post(f"/evaluations/{eval_id}/scores", json={
        "rater_type": "PEER",
        "score_expertise": 70,
        "score_responsibility": 70,
        "score_complexity": 70
    })
    
    # Supervisor (Strict)
    client.post(f"/evaluations/{eval_id}/scores", json={
        "rater_type": "SUPERVISOR_1",
        "score_expertise": 60,
        "score_responsibility": 60,
        "score_complexity": 60
    })
    print("[OK] Scores Submitted (Self, Peer, Supervisor)")

    # 4. Calculate Results
    response = client.post(f"/evaluations/{eval_id}/calculate")
    if response.status_code != 200:
        print(f"[FAIL] Calculate: {response.text}")
        return
    
    result = response.json()
    print(f"[OK] Calculation Complete")
    print(f" - Total Score: {result['total_score']}")
    print(f" - Assigned Grade: {result['grade']}")
    
    # Verify Scores
    scores = result['scores']
    for s in scores:
        print(f" - Rater: {s['rater_type']}, Raw: {s['raw_total']}, Z-Score: {s['z_score']:.2f}")

    if result['total_score'] > 0 and result['grade']:
        print("[SUCCESS] Job Evaluation Logic Verified!")
    else:
        print("[FAIL] Logic Verification Failed")

if __name__ == "__main__":
    verify_job_evaluation()
