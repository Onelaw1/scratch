from fastapi.testclient import TestClient
from backend.main import app
from backend.dependencies import require_roles, require_permission
import uuid

from backend.dependencies import get_current_user
from backend.database import get_db
from backend.models import User

# Mock User
mock_user_id = str(uuid.uuid4())
def mock_get_current_user():
    return {
        "id": mock_user_id,
        "name": "Test Admin",
        "roles": ["ADMIN", "HR_MANAGER"],
        "email": "admin@test.com",
        "institution_id": "inst-001",
        "org_unit_id": "org-001"
    }

app.dependency_overrides[get_current_user] = mock_get_current_user
# Remove faulty require_roles override attempts
app.dependency_overrides.pop(require_roles, None)
app.dependency_overrides.pop(require_permission, None)

client = TestClient(app)

def generate_uuid():
    return str(uuid.uuid4())

def verify_deep_evaluation():
    print("Starting Deep Evaluation Verification...")

    # 1. Setup Data
    inst_id = generate_uuid()
    client.post("/institutions/", json={"id": inst_id, "name": "Deep Eval Inst", "code": f"DEEP_{inst_id[:5]}"})
    
    # 2. Users & Jobs
    rater_id = generate_uuid()
    client.post("/users/", json={"id": rater_id, "institution_id": inst_id, "org_unit_id": generate_uuid(), "email": f"rater_{rater_id[:5]}@test.com", "name": "Rater One"})
    
    target_job_id = generate_uuid()
    # Create required hierarchy for job
    grp = generate_uuid()
    client.post("/jobs/groups/", json={"id": grp, "name": "G1"})
    ser = generate_uuid()
    client.post("/jobs/series/", json={"id": ser, "group_id": grp, "name": "S1"})
    
    client.post("/jobs/positions/", json={"id": target_job_id, "series_id": ser, "title": "Target Job", "grade": "G3"})

    # 3. Create Session
    session_response = client.post("/sessions/", json={
        "institution_id": inst_id,
        "name": "2024 Deep Eval",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    })
    session_id = session_response.json()["id"]
    print(f"[OK] Session Created: {session_id}")

    # 4. Create Assignment (Admin API)
    assign_payload = [{
        "session_id": session_id,
        "rater_user_id": rater_id,
        "target_job_position_id": target_job_id,
        "rater_role": "PEER"
    }]
    resp = client.post("/admin/evaluations/assignments", json=assign_payload)
    if resp.status_code != 200:
        print(f"[FAIL] Assignment Creation: {resp.text}")
        return
    print(f"[OK] Assignment Created")

    # 5. Dry Run Submission (Impact Analysis)
    submission_payload = {
        "session_id": session_id,
        "rater_type": "PEER",
        "rater_user_id": rater_id,
        "ratings": [
            {
                "job_position_id": target_job_id,
                "factor_scores": {"c1": 9, "c2": 9} # Leniency
            }
        ]
    }
    
    resp = client.post(f"/sessions/{session_id}/matrix_submission?dry_run=true", json=submission_payload)
    if resp.status_code != 200:
        print(f"[FAIL] Dry Run: {resp.text}")
    else:
        data = resp.json()
        print(f"[OK] Dry Run Result: {data.get('analysis', 'No Analysis')}")
        if data.get('analysis') and data['analysis']['average'] == 9.0:
             print("[SUCCESS] Analysis Calculation is Correct")
        else:
             print("[FAIL] Analysis Calculation Incorrect")

    # 6. Negative Test (Unassigned Job)
    unassigned_job_id = generate_uuid()
    client.post("/jobs/positions/", json={"id": unassigned_job_id, "series_id": ser, "title": "Unassigned Job", "grade": "G3"})
    
    neg_payload = {
        "session_id": session_id,
        "rater_type": "PEER",
        "rater_user_id": rater_id,
        "ratings": [
            {
                "job_position_id": unassigned_job_id,
                "factor_scores": {"c1": 5}
            }
        ]
    }
    resp = client.post(f"/sessions/{session_id}/matrix_submission", json=neg_payload)
    data = resp.json()
    if data['processed_count'] == 0:
        print("[SUCCESS] Negative Test Passed (Unassigned job skipped)")
    else:
         print(f"[FAIL] Negative Test Failed. Processed Count: {data['processed_count']}")

if __name__ == "__main__":
    verify_deep_evaluation()
