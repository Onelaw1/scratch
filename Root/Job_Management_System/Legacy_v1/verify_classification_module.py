
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, JobGroup, JobSeries, JobPosition, JobTask, WorkItem
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import get_db

# Setup in-memory DB for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=None) # poolclass=None for single connection in memory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Global session for testing to ensure data persistence across requests in memory DB
test_db = TestingSessionLocal()

def override_get_db():
    try:
        yield test_db
    finally:
        pass # Do not close, keep alive for test duration

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_classification_module():
    print("Testing Classification Module...")
    # Use the SAME session
    db = test_db
    
    # 1. Setup Data (5-Depth Hierarchy)
    group = JobGroup(id="g1", name="IT Group")
    db.add(group)
    
    series = JobSeries(id="s1", group_id="g1", name="Software Development")
    db.add(series)
    
    position = JobPosition(id="p1", series_id="s1", title="Backend Engineer")
    db.add(position)
    
    task = JobTask(id="t1", job_position_id="p1", task_name="API Development")
    db.add(task)
    
    item = WorkItem(id="w1", job_task_id="t1", name="Design REST Endpoints")
    db.add(item)
    
    db.commit()
    
    # Debug: Check insertion
    print(f"Debug: Groups: {db.query(JobGroup).count()}")
    print(f"Debug: Series: {db.query(JobSeries).count()}")
    print(f"Debug: Positions: {db.query(JobPosition).count()}")
    print(f"Debug: Tasks: {db.query(JobTask).count()}")
    print(f"Debug: WorkItems: {db.query(WorkItem).count()}")
    
    # 2. Test Tree View
    print("Testing Tree View (/classification/hierarchy)...")
    response = client.get("/classification/hierarchy")
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Tree View Retrieved: {len(data)} groups")
        # Verify structure
        if (data[0]['name'] == "IT Group" and 
            data[0]['children'][0]['name'] == "Software Development" and
            data[0]['children'][0]['children'][0]['name'] == "Backend Engineer" and
            data[0]['children'][0]['children'][0]['children'][0]['name'] == "API Development" and
            data[0]['children'][0]['children'][0]['children'][0]['children'][0]['name'] == "Design REST Endpoints"):
            print("[OK] Hierarchy Structure Verified")
        else:
            print("[FAIL] Hierarchy Structure Incorrect")
    else:
        print(f"[FAIL] Tree View Failed: {response.text}")

    # 3. Test Matrix View
    print("Testing Matrix View (/classification/matrix)...")
    response = client.get("/classification/matrix")
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Matrix View Retrieved: {len(data)} rows")
        if (data[0]['group_name'] == "IT Group" and 
            data[0]['work_item_name'] == "Design REST Endpoints"):
            print("[OK] Matrix Data Verified")
        else:
            print("[FAIL] Matrix Data Incorrect")
    else:
        print(f"[FAIL] Matrix View Failed: {response.text}")

if __name__ == "__main__":
    try:
        test_classification_module()
    except Exception as e:
        print(f"[ERROR] Error: {e}")
