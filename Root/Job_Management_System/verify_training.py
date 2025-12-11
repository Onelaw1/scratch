from fastapi.testclient import TestClient
from backend.main import app
from backend import models, schemas
from backend.database import get_db, Base, engine
import uuid
from datetime import date

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

def verify_training_module():
    print("Starting Training Management Verification (TestClient)...")

    # 1. Create Prerequisites (Institution, OrgUnit, User)
    inst_data = {"name": "Test Inst", "code": f"TEST_{generate_uuid()[:5]}", "category": "MARKET"}
    inst_res = client.post("/institutions/", json=inst_data)
    inst_id = inst_res.json()["id"]

    org_data = {"name": "HR Team", "unit_type": "TEAM", "institution_id": inst_id}
    org_res = client.post("/api/workflow/organizational-units", json=org_data)
    org_id = org_res.json()["id"]

    user_data = {"email": f"user_{generate_uuid()[:5]}@example.com", "name": "Jane Doe", "institution_id": inst_id, "org_unit_id": org_id, "title": "Staff"}
    user_res = client.post("/users/", json=user_data)
    user_id = user_res.json()["id"]
    print("[OK] Prerequisites Created")

    # 2. Create Training Program
    program_data = {
        "name": "Advanced Python for Data Analysis",
        "description": "Learn Pandas and NumPy",
        "duration_hours": 40.0,
        "required_competency": "Python Basics"
    }
    prog_res = client.post("/api/training/programs", json=program_data)
    if prog_res.status_code != 200:
        print(f"Failed to create program: {prog_res.text}")
        return
    program_id = prog_res.json()["id"]
    print(f"[OK] Training Program Created: {program_id}")

    # 3. Assign Training to User
    assign_data = {
        "user_id": user_id,
        "program_id": program_id,
        "status": "PLANNED"
    }
    assign_res = client.post("/api/training/assign", json=assign_data)
    if assign_res.status_code != 200:
        print(f"Failed to assign training: {assign_res.text}")
        return
    training_id = assign_res.json()["id"]
    print(f"[OK] Training Assigned: {training_id}")

    # 4. Update Status to COMPLETED
    update_data = {
        "status": "COMPLETED",
        "completion_date": str(date.today()),
        "score": 95.0
    }
    update_res = client.put(f"/api/training/status/{training_id}", json=update_data)
    if update_res.status_code != 200:
        print(f"Failed to update status: {update_res.text}")
        return
    print("[OK] Training Status Updated to COMPLETED")

    # 5. Verify User History
    history_res = client.get(f"/api/training/user/{user_id}")
    history = history_res.json()
    
    assert len(history) == 1
    assert history[0]["status"] == "COMPLETED"
    assert history[0]["score"] == 95.0
    
    print(f"[OK] User History Verified: {len(history)} record(s)")
    print("[SUCCESS] Training Management Logic Verified!")

if __name__ == "__main__":
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    verify_training_module()
