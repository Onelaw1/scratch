
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, Institution, User, WorkloadEntry, JobTask, JobPosition
from backend.schemas import WorkloadEntryCreate
from backend.routers.workforce import calculate_fte, get_productivity_analysis, get_trend_analysis
from fastapi.testclient import TestClient
from backend.main import app

# Setup file-based DB for debugging
SQLALCHEMY_DATABASE_URL = "sqlite:///test_workforce.db"
if os.path.exists("test_workforce.db"):
    os.remove("test_workforce.db")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[override_get_db] = override_get_db
client = TestClient(app)

def test_workforce_module():
    print("Testing Workforce Module...")
    db = TestingSessionLocal()
    
    # 1. Setup Data
    inst = Institution(id="inst1", name="Test Inst", code="TEST")
    db.add(inst)
    user = User(id="user1", institution_id="inst1", name="Test User", email="test@example.com", org_unit_id="unit1")
    db.add(user)
    
    # Need a JobTask for foreign key
    # And JobPosition
    # And JobSeries
    # And JobGroup... let's just mock what we need or insert minimal data
    # Actually, WorkloadEntry needs task_id and user_id.
    # Let's insert a dummy task.
    # But wait, JobTask needs JobPosition...
    # Let's bypass complex relationships if possible or create minimal chain.
    
    # Minimal chain:
    # Group -> Series -> Position -> Task
    from backend.models import JobGroup, JobSeries
    
    group = JobGroup(id="g1", name="Group 1")
    db.add(group)
    series = JobSeries(id="s1", group_id="g1", name="Series 1")
    db.add(series)
    pos = JobPosition(id="p1", series_id="s1", title="Pos 1")
    db.add(pos)
    task = JobTask(id="t1", job_position_id="p1", task_name="Task 1")
    db.add(task)
    
    db.commit()
    
    # 2. Test FTE Calculation
    print("Testing FTE Calculation...")
    response = client.post("/workforce/calculate-fte", json={
        "user_id": "user1",
        "task_id": "t1",
        "volume": 100,
        "standard_time": 2.0 # 2 hours * 100 = 200 hours. FTE = 200 / 1920 = ~0.104
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] FTE Calculated: {data['fte']}")
        expected_fte = (100 * 2.0) / 1920.0
        if abs(data['fte'] - expected_fte) < 0.001:
             print("[OK] FTE Calculation Correct")
        else:
             print(f"[FAIL] FTE Calculation Incorrect. Expected {expected_fte}, got {data['fte']}")
    else:
        print(f"[FAIL] FTE Calculation Failed: {response.text}")

    # 3. Test Productivity Analysis
    # print("Testing Productivity Analysis...")
    # response = client.get("/workforce/productivity-analysis/inst1")
    # if response.status_code == 200:
    #     data = response.json()
    #     print(f"[OK] Productivity Analysis: {data}")
    #     if data['current_headcount'] == 1 and data['required_fte'] > 0:
    #          print("[OK] Analysis Data Correct")
    #     else:
    #          print("[FAIL] Analysis Data Unexpected")
    # else:
    #     print(f"[FAIL] Productivity Analysis Failed: {response.text}")

    # 4. Test Trend Analysis
    print("Testing Trend Analysis...")
    response = client.get("/workforce/trend-analysis/inst1")
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Trend Analysis: {data}")
        if len(data['projections']) == 5:
             print("[OK] Projections Generated")
        else:
             print("[FAIL] Projections Missing")
    else:
        print(f"[FAIL] Trend Analysis Failed: {response.text}")

if __name__ == "__main__":
    try:
        test_workforce_module()
    except Exception as e:
        print(f"[ERROR] Error: {e}")
