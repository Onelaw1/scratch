import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add Root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "Downloads/Root")))

# Mock missing dependencies
from unittest.mock import MagicMock
from pydantic import BaseModel

class JobDescription(BaseModel): 
    pass
class JobClassification(BaseModel): 
    pass
class JobEvaluation(BaseModel): 
    def calculate_score(self):
        pass
class WorkloadAnalysis(BaseModel): 
    def calculate_gap(self):
        pass

sys.modules["src"] = MagicMock()
sys.modules["src.input"] = MagicMock()
sys.modules["src.input.ncs_client"] = MagicMock()
sys.modules["src.analysis"] = MagicMock()
sys.modules["src.analysis.job_schema"] = MagicMock()
sys.modules["src.analysis.job_schema"].JobDescription = JobDescription
sys.modules["src.analysis.job_schema"].JobClassification = JobClassification
sys.modules["src.analysis.job_schema"].JobEvaluation = JobEvaluation
sys.modules["src.analysis.job_schema"].WorkloadAnalysis = WorkloadAnalysis

from backend.main import app
from backend.database import Base, get_db
from backend.models import Institution, JobGroup, JobSeries, JobPosition, JobTaskNew, WorkItem

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_classification.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_classification_matrix():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # 1. Update (Create) Matrix Data
    payload = [
        {
            "job_group_code": "JG01", "job_group_name": "Management",
            "job_series_code": "JS01", "job_series_name": "HR",
            "job_position_code": "JP01", "job_position_name": "Recruiter",
            "task_code": "JT01", "task_name": "Recruiting",
            "work_code": "WI01", "work_name": "Resume Review",
            "frequency": "DAILY", "workload": 2.0
        },
        {
            "job_group_code": "JG01", "job_group_name": "Management",
            "job_series_code": "JS01", "job_series_name": "HR",
            "job_position_code": "JP01", "job_position_name": "Recruiter",
            "task_code": "JT01", "task_name": "Recruiting",
            "work_code": "WI02", "work_name": "Interview",
            "frequency": "WEEKLY", "workload": 5.0
        }
    ]
    
    print("Sending POST request...")
    response = client.post("/job-centric/classification/matrix", json=payload)
    if response.status_code != 200:
        print(f"POST failed: {response.text}")
    assert response.status_code == 200
    
    # 2. Verify Data Persistence
    print("Sending GET request...")
    response = client.get("/job-centric/classification/matrix")
    assert response.status_code == 200
    data = response.json()
    
    print(f"Received {len(data)} rows")
    assert len(data) == 2
    
    row1 = next(r for r in data if r['work_code'] == 'WI01')
    assert row1['work_name'] == "Resume Review"
    assert row1['job_group_name'] == "Management"
    
    print("Classification Matrix verification passed!")

if __name__ == "__main__":
    # Cleanup start
    engine.dispose()
    if os.path.exists("./test_classification.db"):
        os.remove("./test_classification.db")
        
    try:
        test_classification_matrix()
    except Exception as e:
        print(f"Verification failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup end
        engine.dispose()
        if os.path.exists("./test_classification.db"):
            os.remove("./test_classification.db")
