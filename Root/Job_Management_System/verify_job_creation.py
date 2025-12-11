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

# Mock classes to avoid import errors if dependencies are missing
class JobDescription(BaseModel): pass
class JobClassification(BaseModel): pass
class JobEvaluation(BaseModel): 
    def calculate_score(self): pass
class WorkloadAnalysis(BaseModel): 
    def calculate_gap(self): pass

sys.modules["src"] = MagicMock()
sys.modules["src.input"] = MagicMock()
sys.modules["src.input.ncs_client"] = MagicMock()
sys.modules["src.analysis"] = MagicMock()
sys.modules["src.analysis.job_schema"] = MagicMock()
sys.modules["src.analysis.job_schema"].JobDescription = JobDescription
sys.modules["src.analysis.job_schema"].JobClassification = JobClassification
sys.modules["src.analysis.job_schema"].JobEvaluation = JobEvaluation
sys.modules["src.analysis.job_schema"].JobEvaluation = JobEvaluation
sys.modules["src.analysis.job_schema"].WorkloadAnalysis = WorkloadAnalysis

# Mock services and models for reporting.py
sys.modules["src.services"] = MagicMock()
sys.modules["src.services.data_ingestion_service"] = MagicMock()
sys.modules["src.services.data_ingestion_service"].DataIngestionService = MagicMock()
sys.modules["src.services.pptx_service"] = MagicMock()
sys.modules["src.services.pptx_service"].PPTXService = MagicMock()

sys.modules["src.models"] = MagicMock()
sys.modules["src.models.schema"] = MagicMock()
sys.modules["src.models.schema"].PresentationSchema = MagicMock()
sys.modules["src.models.schema"].SlideContent = MagicMock()

from backend.main import app
from backend.database import Base, get_db
from backend.models import Institution, JobGroup, JobSeries, JobPosition, Job

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_job_creation.db"
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

def test_job_creation_with_hierarchy():
    # Ensure tables exist
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # 1. Create Institution
    inst_res = client.post("/institutions/", json={
        "name": "Test Inst",
        "code": "TEST001",
        "category_type": "MARKET",
        "evaluation_group": "SOC"
    })
    assert inst_res.status_code == 200
    inst_id = inst_res.json()["id"]

    # 2. Create Hierarchy (Group -> Series -> Position)
    group_res = client.post("/organization/groups", json={
        "institution_id": inst_id,
        "code": "JG01",
        "name": "Test Group"
    })
    assert group_res.status_code == 200
    group_id = group_res.json()["id"]

    series_res = client.post("/organization/series", json={
        "job_group_id": group_id,
        "code": "JS01",
        "name": "Test Series"
    })
    assert series_res.status_code == 200
    series_id = series_res.json()["id"]

    pos_res = client.post("/organization/positions", json={
        "job_series_id": series_id,
        "code": "JP01",
        "name": "Test Position"
    })
    assert pos_res.status_code == 200
    pos_id = pos_res.json()["id"]

    # 3. Create Job with job_position_id
    # Need to create a department first
    # But for simplicity, let's assume department_id is handled or mocked if needed.
    # Looking at models.py, Department is required.
    # Let's create a dummy department if there's an endpoint, or just insert it directly.
    # There is no explicit department endpoint in the routers list I saw earlier (except maybe in institutions or organization?)
    # Wait, models.py has Department. Let's check if we can create one.
    # If not, I'll insert it via DB session directly.
    
    db = TestingSessionLocal()
    from backend.models import Department
    dept = Department(institution_id=inst_id, name="Test Dept", code="DEPT01")
    db.add(dept)
    db.commit()
    dept_id = dept.id
    db.close()

    job_payload = {
        "title": "Test Job",
        "department_id": dept_id,
        "job_position_id": pos_id,
        "ncs_code": "NCS001",
        "description": "Test Description"
    }

    print("Creating Job...")
    job_res = client.post(f"/jobs/{inst_id}", json=job_payload)
    if job_res.status_code != 200:
        print(f"Job creation failed: {job_res.text}")
    assert job_res.status_code == 200
    job_data = job_res.json()
    
    assert job_data["job_position_id"] == pos_id
    print("Job created successfully with job_position_id!")

    # 4. Verify Persistence
    get_res = client.get(f"/jobs/{inst_id}")
    assert get_res.status_code == 200
    jobs = get_res.json()
    assert len(jobs) == 1
    assert jobs[0]["job_position_id"] == pos_id
    print("Verification passed!")

if __name__ == "__main__":
    try:
        test_job_creation_with_hierarchy()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        engine.dispose()
        if os.path.exists("./test_job_creation.db"):
            os.remove("./test_job_creation.db")
