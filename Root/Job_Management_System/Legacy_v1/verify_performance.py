from fastapi.testclient import TestClient
from backend.main import app
from backend import models, schemas
from backend.database import get_db, Base, engine
import uuid

# Override Dependency
def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def generate_uuid():
    return str(uuid.uuid4())

def verify_performance_module():
    print("Starting Performance Evaluation Verification (TestClient)...")

    # 1. Create Prerequisites (Institution, OrgUnit, User)
    inst_data = {"name": "Test Inst", "code": f"TEST_{generate_uuid()[:5]}", "category": "MARKET"}
    inst_res = client.post("/institutions/", json=inst_data)
    if inst_res.status_code != 200:
        print(f"Failed to create institution: {inst_res.text}")
        return
    inst_id = inst_res.json()["id"]

    org_data = {"name": "HR Team", "unit_type": "TEAM", "institution_id": inst_id}
    org_res = client.post("/api/workflow/organizational-units", json=org_data)
    if org_res.status_code != 200:
        print(f"Failed to create org unit: {org_res.text}")
        return
    org_id = org_res.json()["id"]

    user_data = {"email": f"user_{generate_uuid()[:5]}@example.com", "name": "John Doe", "institution_id": inst_id, "org_unit_id": org_id, "title": "Manager"}
    user_res = client.post("/users/", json=user_data)
    if user_res.status_code != 200:
        print(f"Failed to create user: {user_res.text}")
        return
    user_id = user_res.json()["id"]
    print("[OK] Prerequisites Created")

    # 2. Create Performance Review
    review_data = {
        "user_id": user_id,
        "year": 2024,
        "score_common": 85.0,
        "score_leadership": 80.0
    }
    review_res = client.post("/api/performance/reviews", json=review_data)
    if review_res.status_code != 200:
        print(f"Failed to create review: {review_res.text}")
        return
    review_id = review_res.json()["id"]
    print(f"[OK] Review Created: {review_id}")

    # 3. Add Performance Goals (MBO)
    goals = [
        {"category": "MBO", "goal_text": "Increase Sales", "weight": 40.0, "target": "1M", "actual": "1.2M"},
        {"category": "MBO", "goal_text": "Team Training", "weight": 30.0, "target": "3 Sessions", "actual": "3 Sessions"},
        {"category": "BSC", "goal_text": "Process Improvement", "weight": 30.0, "target": "Reduce time by 10%", "actual": "Reduced by 15%"}
    ]
    
    goal_ids = []
    for g in goals:
        g_res = client.post(f"/api/performance/reviews/{review_id}/goals", json=g)
        goal_ids.append(g_res.json()["id"])
    print("[OK] 3 Goals Added")

    # 4. Update Goal Scores (Supervisor Scoring)
    # Goal 1: 40% * 100 = 40
    client.put(f"/api/performance/goals/{goal_ids[0]}", json={"supervisor_score": 100.0})
    # Goal 2: 30% * 90 = 27
    client.put(f"/api/performance/goals/{goal_ids[1]}", json={"supervisor_score": 90.0})
    # Goal 3: 30% * 80 = 24
    client.put(f"/api/performance/goals/{goal_ids[2]}", json={"supervisor_score": 80.0})
    print("[OK] Goal Scores Updated")

    # 5. Calculate Results
    # Job Score = 40 + 27 + 24 = 91.0
    # Total Score = (91 * 0.6) + (85 * 0.2) + (80 * 0.2) = 54.6 + 17 + 16 = 87.6
    # Grade = A (>= 80)
    calc_res = client.post(f"/api/performance/reviews/{review_id}/calculate")
    result = calc_res.json()
    
    print(f"[OK] Calculation Complete")
    print(f" - Job Score: {result['score_job']} (Expected: 91.0)")
    print(f" - Total Score: {result['total_score']} (Expected: 87.6)")
    print(f" - Grade: {result['grade']} (Expected: A)")

    assert result['score_job'] == 91.0
    assert abs(result['total_score'] - 87.6) < 0.01
    assert result['grade'] == "A"

    # 6. Finalize
    final_res = client.post(f"/api/performance/reviews/{review_id}/finalize")
    assert final_res.json()['status'] == "FINAL"
    print("[SUCCESS] Performance Evaluation Logic Verified!")

if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    verify_performance_module()
