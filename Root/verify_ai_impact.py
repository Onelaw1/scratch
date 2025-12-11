from fastapi import FastAPI
from fastapi.testclient import TestClient
from Job_Management_System.backend.database import Base, engine
from Job_Management_System.backend.routers import job_analysis, ai_impact, jobs
import uuid

# Setup App
app = FastAPI()
app.include_router(job_analysis.router)
app.include_router(ai_impact.router)
app.include_router(jobs.router)

# Setup DB
Base.metadata.create_all(bind=engine)
client = TestClient(app)

def generate_uuid():
    return str(uuid.uuid4())

def verify_ai_impact():
    print("Starting AI Impact Analysis Verification (AI-ADFM)...")
    
    # Prerequisite: Job Group & Series
    group_id = generate_uuid()
    res = client.post("/jobs/groups/", json={"id": group_id, "name": "Test Group"})
    if res.status_code not in [200, 201]:
        print(f"[FAIL] Group Create: {res.text}")
        return

    series_id = generate_uuid()
    res = client.post("/jobs/series/", json={"id": series_id, "group_id": group_id, "name": "Test Series"})
    if res.status_code not in [200, 201]:
        print(f"[FAIL] Series Create: {res.text}")
        return

    # 1. Create Job Position
    pos_id = generate_uuid()
    pos_data = {
        "id": pos_id,
        "series_id": series_id,
        "name": "Policy Analyst (AI Pilot)",
        "is_future_model": True
    }
    res = client.post("/job-analysis/job-positions/", json=pos_data)
    if res.status_code not in [200, 201]:
        print(f"[FAIL] Position Create: {res.text}")
        return
    print(f"[OK] Position Created: {pos_data['name']}")
    
    # 2. Create Tasks with AI Scores
    # Task A: Report Drafting (High Augmentation)
    task_a_id = generate_uuid()
    task_a = {
        "id": task_a_id,
        "position_id": pos_id,
        "task_name": "Policy Report Drafting",
        "ai_substitution": 0.1,  # 10% auto
        "ai_augmentation": 0.8,  # 80% helped
        "ai_generation": 0.2     # 20% new verification work
    }
    res = client.post("/job-analysis/job-tasks/", json=task_a)
    if res.status_code not in [200, 201]:
        print(f"[FAIL] Task A Create: {res.text}")
        return
    
    # Task B: Data Entry (High Substitution)
    task_b_id = generate_uuid()
    task_b = {
        "id": task_b_id,
        "position_id": pos_id,
        "task_name": "Simple Data Entry",
        "ai_substitution": 0.9,  # 90% auto
        "ai_augmentation": 0.0,
        "ai_generation": 0.05    # 5% check
    }
    res = client.post("/job-analysis/job-tasks/", json=task_b)
    if res.status_code not in [200, 201]:
        print(f"[FAIL] Task B Create: {res.text}")
        return
    print("[OK] Tasks Created with AI Scores")
    
    # 3. Create Workload (Volume * ST)
    # Need User first? WorkloadEntryCreate requires user_id. 
    # If FK enforced, we need a user. 
    # Let's create a dummy user if we can, or just pass a UUID if 'users' table is empty and FK not enforced (SQLite default).
    # But since we are using 'job_analysis' router, it might not check user existence if we didn't import user router.
    # However, DB schema has FK.
    # Let's try creating a user. We need 'organization' router for that.
    # Or just try passing UUID.
    
    user_id = generate_uuid()
    
    # Task A: 100 reports * 4 hours = 400 hours
    res = client.post("/job-analysis/workload-entries/", json={
        "user_id": user_id,
        "task_id": task_a_id,
        "volume": 100,
        "standard_time": 4.0
    })
    if res.status_code not in [200, 201]:
        print(f"[FAIL] Workload A Create: {res.text}")
        # If it fails due to User FK, we need to create user.
        # But let's see.
    
    # Task B: 1000 entries * 0.5 hours = 500 hours
    client.post("/job-analysis/workload-entries/", json={
        "user_id": user_id,
        "task_id": task_b_id,
        "volume": 1000,
        "standard_time": 0.5
    })
    print("[OK] Workload Data Submitted")
    
    # 4. Run Simulation
    print("\n[4] Running AI-ADFM Simulation...")
    res = client.post(f"/ai-impact/simulate-fte/{pos_id}?adoption_rate=1.0&efficiency_factor=0.5")
    
    if res.status_code == 200:
        data = res.json()
        print(f"Position: {data['position_name']}")
        print(f"Total FTE (Old): {data['total_fte_old']}")
        print(f"Total FTE (AI):  {data['total_fte_ai']}")
        print(f"Net Change:      {data['net_change_percent']}%")
        
        print("\nBreakdown:")
        for item in data['breakdown']:
            print(f" - {item['task_name']}: Old={item['fte_old']} -> AI={item['fte_ai']} (Gain: {item['efficiency_gain_percent']}%)")
            
        # Validation Logic
        # Task A: 400h. Impact = 0.1 + (0.8*0.5) = 0.5. Gen = 0.2. Net Factor = 1 - 0.5 + 0.2 = 0.7.
        # Expected A Hours = 400 * 0.7 = 280.
        # Task B: 500h. Impact = 0.9 + 0 = 0.9. Gen = 0.05. Net Factor = 1 - 0.9 + 0.05 = 0.15.
        # Expected B Hours = 500 * 0.15 = 75.
        # Total AI Hours = 355.
        # Total Old Hours = 900.
        # Expected FTE AI = 355 / 1920 = 0.1849
        # Expected FTE Old = 900 / 1920 = 0.46875
        
        if abs(data['total_fte_ai'] - 0.1849) < 0.01:
            print("\n[SUCCESS] Simulation Logic Verified!")
        else:
            print(f"\n[FAIL] Logic Mismatch. Expected ~0.1849, Got {data['total_fte_ai']}")
            
    else:
        print(f"[FAIL] Simulation API Error: {res.text}")

if __name__ == "__main__":
    verify_ai_impact()
