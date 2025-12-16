import sys
import os
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add Root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from backend.main import app
from backend.database import Base, get_db
from backend import models

# Setup In-Memory DB
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def setup_data():
    db = TestingSessionLocal()
    
    # 1. Setup User & Job for Dashboard
    # Org
    org_hr = models.OrgUnit(id="org_hr", name="Human Resources Team", unit_type="TEAM", budget=0, authorized_headcount=0)
    org_strat = models.OrgUnit(id="org_strat", name="Strategic Planning Team", unit_type="TEAM", budget=1000, authorized_headcount=6)
    db.add(org_hr)
    db.add(org_strat)
    
    # Job
    pos = models.JobPosition(id="pos_dev", title="Developer", grade="G3")
    db.add(pos)
    
    task1 = models.JobTask(id="task_1", job_position_id="pos_dev", task_name="Coding")
    task2 = models.JobTask(id="task_2", job_position_id="pos_dev", task_name="Testing")
    db.add(task1)
    db.add(task2)
    
    # User
    user = models.User(id="user_test", name="Test User", email="test@test.com", org_unit_id="org_strat")
    db.add(user)
    
    # Update Position with User
    pos.user_id = "user_test"
    
    # Training
    prog = models.TrainingProgram(id="prog_py", name="Python Master", duration_hours=10.0)
    db.add(prog)
    
    emp_training = models.EmployeeTraining(
        id="et_1", user_id="user_test", program_id="prog_py", 
        status=models.TrainingStatus.COMPLETED
    )
    db.add(emp_training)
    
    # Goals
    review = models.PerformanceReview(id="rev_1", user_id="user_test", year=2024, status=models.ReviewStatus.DRAFT)
    db.add(review)
    
    goal1 = models.PerformanceGoal(id="goal_1", review_id="rev_1", category="MBO", goal_text="Goal 1")
    goal2 = models.PerformanceGoal(id="goal_2", review_id="rev_1", category="MBO", goal_text="Goal 2")
    db.add(goal1)
    db.add(goal2)
    
    # Institution (for ERP log)
    inst = models.Institution(id="inst_main", name="Main Inst", code="INST001")
    db.add(inst)
    
    db.commit()
    db.close()

def verify_my_job():
    print("\n--- Verifying My Job Dashboard ---")
    res = client.get("/users/me/dashboard")
    if res.status_code != 200:
        print(f"❌ Failed to get dashboard: {res.text}")
        return
        
    data = res.json()
    # Check User
    if data['user']['name'] == "Test User":
        print("[PASS] User Name Verified")
    else:
        print(f"[FAIL] User Name Mismatch: {data['user']['name']}")
        
    # Check Stats
    # Goals = 2
    if data['stats']['goals_completed'] == 2:
        print("[PASS] Goals Count Verified (2)")
    else:
        print(f"[FAIL] Goals Count Mismatch: {data['stats']['goals_completed']}")
        
    # Training = 10.0
    if data['stats']['training_hours'] == 10.0:
        print("[PASS] Training Hours Verified (10.0)")
    else:
        print(f"[FAIL] Training Hours Mismatch: {data['stats']['training_hours']}")

    # Key Tasks
    if "Coding" in data['key_tasks']:
        print("[PASS] Key Tasks Verified")
    else:
        print(f"[FAIL] Key Tasks Missing: {data['key_tasks']}")

def verify_erp_sync():
    print("\n--- Verifying ERP Sync ---")
    
    # 1. Preview
    res = client.get("/erp/preview")
    diffs = res.json()
    
    # We expect 'Strategic Planning Team' to be DIFF
    # Mock says Budget 1200, TO 8. We set up 1000, 6.
    strat_diff = next((d for d in diffs if "Strategic" in d['dept_name']), None)
    if strat_diff and strat_diff['status'] == 'DIFF':
        print("[PASS] Preview Detected DIFF correctly")
    else:
        print(f"[FAIL] Preview Failed: {strat_diff}")
        
    # 2. Sync
    res = client.post("/erp/sync")
    sync_res = res.json()
    if sync_res['status'] == "success" and sync_res['updated'] >= 1:
        print(f"[PASS] Sync Executed: Updated {sync_res['updated']} records")
    else:
        print(f"[FAIL] Sync Failed: {sync_res}")
        
    # 3. Verify Update in DB
    db = TestingSessionLocal()
    org = db.query(models.OrgUnit).filter(models.OrgUnit.id == "org_strat").first()
    if org.budget == 1200 and org.authorized_headcount == 8:
        print("[PASS] DB Record Updated Successfully")
    else:
        print(f"[FAIL] DB Record Not Updated: B={org.budget}, TO={org.authorized_headcount}")
    db.close()

if __name__ == "__main__":
    setup_data()
    verify_my_job()
    verify_erp_sync()
