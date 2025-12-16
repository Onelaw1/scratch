import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add Root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from backend.main import app
from backend.database import Base, get_db
from backend.models import User, Institution, OrgUnit
from backend import models

# Setup Test DB
import uuid
import os
from sqlalchemy.pool import StaticPool

# Setup Test DB
SQLALCHEMY_DATABASE_URL = "sqlite://" # In-memory
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
    
    # 1. Institution
    inst = Institution(id="inst_prod", name="Prod Corp", code="PC001")
    db.add(inst)
    
    # 2. Org & User
    org = OrgUnit(id="org_prod", institution_id="inst_prod", name="Biz Team", unit_type="TEAM")
    db.add(org)
    
    user = User(id="user_prod_1", institution_id="inst_prod", org_unit_id="org_prod", email="prod@test.com", name="Prod User")
    db.add(user)
    
    db.commit()
    db.close()

def test_productivity_metrics():
    setup_data()
    
    print("\n--- Testing Productivity Metrics ---")
    
    # 1. Add Workload (FTE)
    print("1. Creating Workload Entry...")
    # Use DB session to avoid API complexity and ensure data is there
    db = TestingSessionLocal()
    from backend.models import JobTask, JobPosition, JobSeries, JobGroup
    
    grp = JobGroup(id="grp_1", name="G")
    ser = JobSeries(id="ser_1", group_id="grp_1", name="S")
    pos = JobPosition(id="pos_1", series_id="ser_1", title="Direct", grade="G1")
    task = JobTask(id="task_1", job_position_id="pos_1", task_name="Work")
    
    db.add_all([grp, ser, pos, task])
    
    # Ensure flush to get IDs if needed (though we set them)
    db.flush()
    
    from backend.models import WorkloadEntry
    # FTE = 1.0 (240 * 8 / 1920)
    wl = WorkloadEntry(id="wl_1", user_id="user_prod_1", task_id="task_1", volume=240, standard_time=8, fte=1.0)
    db.add(wl)
    db.commit()
    db.close()
    
    # 2. Add Financial Data
    print("2. Adding Financial Data...")
    fin_payload = {
        "institution_id": "inst_prod",
        "year": 2024,
        "revenue": 1000000000, 
        "operating_expenses": 400000000, 
        "personnel_costs": 300000000 
    }
    
    res = client.post("/job-analysis/productivity/financial", json=fin_payload)
    if res.status_code != 200:
        print(f"Failed to add fin data: {res.text}")
        return
        
    print("Financial Data Added.")
    
    # 3. Fetch Metrics
    print("3. Fetching Metrics...")
    res = client.get("/job-analysis/productivity/metrics/inst_prod")
    data = res.json()
    print("Metrics Response:", data)
    
    # Validation
    if data['hcroi'] == 2.0:
        print("HCROI Verified: 2.0")
    else:
        print(f"HCROI Mismatch: {data['hcroi']}")
        # Debugging
        db = TestingSessionLocal()
        entries = db.query(models.WorkloadEntry).all()
        print(f"DEBUG: Found {len(entries)} workload entries")
        for e in entries:
            print(f" - Entry: {e.id}, User: {e.user_id}, FTE: {e.fte}")
            user = db.query(models.User).filter(models.User.id == e.user_id).first()
            if user:
                print(f"   -> User Inst: {user.institution_id}")
            else:
                print("   -> User NOT FOUND")
        
        # Test exact query
        from sqlalchemy import func
        total_fte_test = db.query(func.sum(models.WorkloadEntry.fte))\
            .join(models.User, models.WorkloadEntry.user_id == models.User.id)\
            .filter(models.User.institution_id == "inst_prod")\
            .scalar()
        print(f"DEBUG: Exact Query Result locally: {total_fte_test}")
        
        db.close()
        
    if data['total_fte'] == 1.0:
         print("FTE Verified: 1.0")
    else:
         print(f"FTE Mismatch: {data['total_fte']}")

if __name__ == "__main__":
    test_productivity_metrics()
