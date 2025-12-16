
import sys
import os
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add Root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from backend.main import app
from backend.database import Base, get_db
from backend import models

# In-Memory DB
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
    
    # 1. User & Org (Joined 5 years ago)
    hire_date = date.today() - timedelta(days=365*5)
    
    org_hr = models.OrgUnit(id="org_hr", name="HR Team", unit_type="TEAM")
    inst = models.Institution(id="inst_1", name="Public Corp", code="INST001")
    db.add(org_hr)
    db.add(inst)
    
    user = models.User(
        id="user_test", 
        name="Tenure User", 
        email="tenure@test.com", 
        org_unit_id="org_hr",
        hire_date=hire_date
    )
    db.add(user)
    
    # 2. Job Position (Assigned 2 years ago)
    assign_date = date.today() - timedelta(days=365*2)
    
    series = models.JobSeries(id="ser_1", name="General Admin", group_id="grp_1") # Mock group link
    # Need mock group
    group = models.JobGroup(id="grp_1", name="Admin Group")
    db.add(group)
    db.add(series)
    
    pos = models.JobPosition(
        id="pos_mgr", 
        title="HR Manager", 
        series_id="ser_1",
        assignment_date=assign_date,
        user_id="user_test" # Link User
    )
    db.add(pos)
    
    # 3. History Logs
    # Org History: Hired 5 years ago
    oh = models.OrgHistory(
        id="oh_1", 
        user_id="user_test", 
        org_unit_id="org_hr", 
        start_date=hire_date,
        role_name="New Hire"
    )
    db.add(oh)
    
    # Job History: 2 years ago
    jh = models.JobHistory(
        id="jh_1",
        job_position_id="pos_mgr",
        change_date=assign_date,
        change_type="ASSIGNMENT",
        description="Assigned as Manager"
    )
    db.add(jh)
    
    db.commit()
    db.close()

def verify_pulse_check():
    print("\n--- Verifying Pulse Check ---")
    
    # 1. Post Check-in
    payload = {
        "mood_score": 4,
        "workload_score": 3,
        "energy_score": 5,
        "comment": "Feeling good!"
    }
    res = client.post("/users/me/pulse", json=payload)
    if res.status_code == 200:
        data = res.json()
        print(f"[PASS] Pulse Submitted: ID={data['id']}, Mood={data['mood_score']}")
    else:
        print(f"[FAIL] Pulse Submit Failed: {res.text}")
        
    # 2. Check Dashboard reflect
    res = client.get("/users/me/dashboard")
    data = res.json()
    if data['stats']['pulse_score'] == "🙂": # 4 = 🙂
        print("[PASS] Dashboard shows correct Pulse Emoji")
    else:
        print(f"[FAIL] Dashboard Pulse Mismatch: {data['stats']['pulse_score']}")

def verify_tenure_analysis():
    print("\n--- Verifying Dual Tenure ---")
    
    res = client.get("/personnel/user_test/tenure-analysis")
    if res.status_code == 200:
        data = res.json()
        # Expect Org Tenure ~ 60 months, Job Tenure ~ 24 months
        # Allow small margin
        org_mo = data['org_tenure_months']
        job_mo = data['job_tenure_months']
        
        print(f"Stats: Org={org_mo} mo, Job={job_mo} mo, Ratio={data['expertise_ratio']}")
        
        if 59 <= org_mo <= 61:
            print("[PASS] Org Tenure Correct (~60 months)")
        else:
            print(f"[FAIL] Org Tenure Value Issue: {org_mo}")
            
        if 23 <= job_mo <= 25:
             print("[PASS] Job Tenure Correct (~24 months)")
        else:
            print(f"[FAIL] Job Tenure Value Issue: {job_mo}")
            
    else:
        print(f"[FAIL] Tenure Analysis Failed: {res.text}")

if __name__ == "__main__":
    setup_data()
    verify_pulse_check()
    verify_tenure_analysis()
