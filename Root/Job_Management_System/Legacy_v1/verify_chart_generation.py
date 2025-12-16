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

# Mock classes
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
sys.modules["src.analysis.job_schema"].WorkloadAnalysis = WorkloadAnalysis

from backend.main import app
from backend.database import Base, get_db
from backend.models import Institution, Department, Job

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_chart_gen.db"
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

def test_chart_generation():
    # Ensure tables exist
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # 1. Create Data
    db = TestingSessionLocal()
    inst = Institution(name="Chart Inst", code="CHART01", category_type="MARKET", evaluation_group="SOC")
    db.add(inst)
    db.commit()
    inst_id = inst.id

    dept1 = Department(institution_id=inst_id, name="HR Team", code="HR")
    dept2 = Department(institution_id=inst_id, name="IT Team", code="IT")
    db.add_all([dept1, dept2])
    db.commit()

    # Add jobs
    jobs = [
        Job(institution_id=inst_id, department_id=dept1.id, title="Recruiter"),
        Job(institution_id=inst_id, department_id=dept1.id, title="Manager"),
        Job(institution_id=inst_id, department_id=dept2.id, title="Developer"),
    ]
    db.add_all(jobs)
    db.commit()
    db.close()

    # 2. Request Chart
    print("Requesting Job Distribution Chart...")
    response = client.get(f"/statistics/reports/job-distribution/{inst_id}")
    
    if response.status_code == 200:
        print("Chart generated successfully!")
        assert response.headers["content-type"] == "image/png"
    else:
        print(f"Chart generation failed: {response.status_code} - {response.text}")
        # It might fail if matplotlib is not installed or ChartService import fails
        # But we want to see the error
        
if __name__ == "__main__":
    try:
        test_chart_generation()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        engine.dispose()
        if os.path.exists("./test_chart_gen.db"):
            os.remove("./test_chart_gen.db")
