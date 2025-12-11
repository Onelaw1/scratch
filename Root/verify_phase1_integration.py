from fastapi import FastAPI
from fastapi.testclient import TestClient
from Job_Management_System.backend.database import Base, engine
from Job_Management_System.backend.routers import job_analysis
import uuid

# 1. Create Standalone App for Verification
app = FastAPI()
app.include_router(job_analysis.router)

# 2. Setup Test DB
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def generate_uuid():
    return str(uuid.uuid4())

def verify_integration():
    print("Starting Phase 1 Integration Verification (Isolated)...")
    
    # 1. Setup Data (OrgUnit, JobPosition)
    print("\n[1] Setting up prerequisite data...")
    
    inst_id = generate_uuid()
    org_id = generate_uuid()
    org_data = {
        "id": org_id,
        "institution_id": inst_id,
        "name": "HR Team",
        "unit_type": "TEAM",
        "mission": "Manage Human Resources"
    }
    
    res = client.post("/job-analysis/org-units/", json=org_data)
    if res.status_code in [200, 201]:
        print(f"[OK] OrgUnit created: {org_data['name']}")
    else:
        print(f"[FAIL] OrgUnit creation failed: {res.text}")

    # Create JobPosition
    series_id = generate_uuid()
    pos_id = generate_uuid()
    pos_data = {
        "id": pos_id,
        "series_id": series_id,
        "name": "HR Manager",
        "is_future_model": False
    }
    res = client.post("/job-analysis/job-positions/", json=pos_data)
    if res.status_code in [200, 201]:
        print(f"[OK] JobPosition created: {pos_data['name']}")
    else:
        print(f"[FAIL] JobPosition creation failed: {res.text}")
    
    # 2. Create Job Task
    print("\n[2] Creating Job Task (Auto-complete Source)...")
    task_id = generate_uuid()
    task_data = {
        "id": task_id,
        "position_id": pos_id,
        "task_name": "Recruitment Planning",
        "action_verb": "Plan",
        "task_object": "Recruitment"
    }
    res = client.post("/job-analysis/job-tasks/", json=task_data)
    if res.status_code in [200, 201]:
        print(f"[OK] JobTask created: {task_data['task_name']}")
    else:
        print(f"[FAIL] JobTask creation failed: {res.text}")

    # 3. Verify Auto-complete Fetch
    print("\n[3] Verifying Auto-complete Fetch...")
    res = client.get("/job-analysis/job-tasks/")
    if res.status_code == 200:
        tasks = res.json()
        found = any(t['task_name'] == "Recruitment Planning" for t in tasks)
        if found:
            print(f"[OK] Auto-complete API returned the created task.")
        else:
            print(f"[FAIL] Created task not found in list.")
    else:
        print(f"[FAIL] Failed to fetch tasks: {res.text}")

    # 4. Submit Workload Entry (Grid Save)
    print("\n[4] Submitting Workload Entry (Grid Save)...")
    user_id = generate_uuid()
    entry_data = {
        "user_id": user_id,
        "task_id": task_id,
        "volume": 100,
        "standard_time": 2.5
    }
    
    res = client.post("/job-analysis/workload-entries/", json=entry_data)
    if res.status_code in [200, 201]:
        entry = res.json()
        print(f"[OK] WorkloadEntry saved.")
        
        # 5. Verify FTE Calculation
        print("\n[5] Verifying FTE Calculation...")
        expected_fte = (100 * 2.5) / 1920
        actual_fte = entry['fte']
        print(f"  - Input: Volume=100, ST=2.5")
        print(f"  - Expected FTE: {expected_fte:.4f}")
        print(f"  - Actual FTE:   {actual_fte:.4f}")
        
        if abs(actual_fte - expected_fte) < 0.0001:
            print("[OK] FTE Calculation is CORRECT.")
        else:
            print("[FAIL] FTE Calculation is INCORRECT.")
    else:
        print(f"[FAIL] WorkloadEntry creation failed: {res.text}")

if __name__ == "__main__":
    verify_integration()
