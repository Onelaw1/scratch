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

# Setup Test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_productivity.db"
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
    # User works 8 hours daily = 1 FTE roughly
    # 8 hours * 240 days = 1920 hours
    print("1. Creating Workload Entry...")
    client.post("/job-analysis/workload-entries/", json={
        "user_id": "user_prod_1",
        "task_id": "dummy_task_id", # Not enforced by FK in this simplistic test unless model strictness
        # Wait, task_id is FK. Need a task.
        # Let's create a task first.
        "volume": 240, 
        "standard_time": 8.0, 
        # FTE should be 1.0
        "task_id": "temp_task_id" # This will fail if FK constraint is active in sqlite? Yes usually.
    })
    
    # Let's do it properly via API or DB.
    # We might need to create a Job Position and Task first to be safe.
    
    # 2. Add Financial Data
    print("2. Adding Financial Data...")
    fin_payload = {
        "institution_id": "inst_prod",
        "year": 2024,
        "revenue": 1000000000, # 10억
        "operating_expenses": 400000000, # 4억
        "personnel_costs": 300000000 # 3억
    }
    # Net Income = 10 - 4 - 3 = 3억
    # Adjusted Revenue = 10 - 4 = 6억
    # HCROI = 6억 / 3억 = 2.0
    
    res = client.post("/job-analysis/productivity/financial", json=fin_payload)
    if res.status_code != 200:
        print(f"Failed to add fin data: {res.text}")
        return
        
    print("Financial Data Added.")
    
    # 3. Get Metrics
    # But wait, we didn't successfully create workload because of FK.
    # For this test, let's just Insert Workload manually into DB to bypass complex setup if possible, 
    # OR Create the task properly.
    
    # Actually, let's use the DB session to insert a dummy task and workload to ensure FK is happy.
    db = TestingSessionLocal()
    from backend.models import JobTask, JobPosition, JobSeries, JobGroup
    
    grp = JobGroup(id="grp_1", name="G")
    ser = JobSeries(id="ser_1", group_id="grp_1", name="S")
    pos = JobPosition(id="pos_1", series_id="ser_1", title="Direct", grade="G1")
    task = JobTask(id="task_1", job_position_id="pos_1", task_name="Work")
    
    db.add_all([grp, ser, pos, task])
    from backend.models import WorkloadEntry
    # FTE = 1.0
    wl = WorkloadEntry(id="wl_1", user_id="user_prod_1", task_id="task_1", volume=240, standard_time=8, fte=1.0)
    db.add(wl)
    db.commit()
    db.close()
    
    print("3. Fetching Metrics...")
    res = client.get("/job-analysis/productivity/metrics/inst_prod")
    data = res.json()
    print("Metrics Response:", data)
    
    # Validation
    # HCROI expected: 2.0
    # HCVA expected: 600,000,000 / 1.0 = 600,000,000
    if data['hcroi'] == 2.0:
        print("✅ HCROI Verified: 2.0")
    else:
        print(f"❌ HCROI Mismatch: {data['hcroi']}")
        
    if data['total_fte'] == 1.0:
         print("✅ FTE Verified: 1.0")
    else:
         print(f"❌ FTE Mismatch: {data['total_fte']}")

if __name__ == "__main__":
    try:
        if os.path.exists("./test_productivity.db"):
            os.remove("./test_productivity.db")
        test_productivity_metrics()
    finally:
        if os.path.exists("./test_productivity.db"):
            os.remove("./test_productivity.db")
