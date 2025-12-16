import sys
import os
import sys
import os
# import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add Root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "Downloads/Root")))

from backend.main import app
from backend.database import Base, get_db
from backend.models import User, Institution, Department

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_workload.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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

def setup_test_data():
    db = TestingSessionLocal()
    # Create Institution
    inst = Institution(id="inst_1", name="Test Inst", code="TI01", category_type="MARKET", evaluation_group="SOC")
    db.add(inst)
    
    # Create Department
    dept = Department(id="dept_1", institution_id="inst_1", name="IT Team")
    db.add(dept)
    
    # Create User
    user = User(id="emp_1", institution_id="inst_1", department_id="dept_1", email="test@example.com", name="Test User")
    db.add(user)
    
    db.commit()
    db.close()

def test_workload_flow():
    # Setup
    setup_test_data()
    
    # 1. Get initial survey (should be empty but user exists)
    response = client.get("/job-centric/workload/survey")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    user_data = next(d for d in data if d['id'] == 'emp_1')
    assert user_data['name'] == "Test User"
    assert len(user_data['tasks']) == 0
    
    # 2. Update workload
    payload = {
        "id": "emp_1",
        "name": "Test User",
        "department": "IT Team",
        "tasks": [
            {
                "name": "Coding",
                "frequency": "DAILY",
                "hoursPerOccurrence": 4.0,
                "totalHours": 960.0
            },
            {
                "name": "Meeting",
                "frequency": "WEEKLY",
                "hoursPerOccurrence": 2.0,
                "totalHours": 96.0
            }
        ],
        "totalHours": 1056.0
    }
    
    response = client.post("/job-centric/workload/survey/emp_1", json=payload)
    assert response.status_code == 200
    updated_data = response.json()
    assert len(updated_data['tasks']) == 2
    assert updated_data['totalHours'] == 1056.0
    
    # 3. Verify persistence
    response = client.get("/job-centric/workload/survey")
    assert response.status_code == 200
    data = response.json()
    user_data = next(d for d in data if d['id'] == 'emp_1')
    assert len(user_data['tasks']) == 2
    assert user_data['tasks'][0]['name'] == "Coding"

if __name__ == "__main__":
    # Clean up old test db
    if os.path.exists("./test_workload.db"):
        os.remove("./test_workload.db")
        
    try:
        test_workload_flow()
        print("✅ Workload API verification passed!")
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if os.path.exists("./test_workload.db"):
            os.remove("./test_workload.db")
