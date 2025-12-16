import sys
import os
import uuid
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from backend.main import app

client = TestClient(app)

def generate_uuid():
    return str(uuid.uuid4())

def verify_organization_api():
    print("Starting Organization API Verification...")
    
    # 1. Create Institution (Prerequisite)
    print("\n1. Creating Institution...")
    inst_code = f"INST_{generate_uuid()[:8]}"
    inst_payload = {
        "name": "Test Institution",
        "code": inst_code,
        "category_type": "MARKET",
        "evaluation_group": "SOC"
    }
    response = client.post("/institutions/", json=inst_payload)
    if response.status_code != 200:
        print(f"   Failed to create institution: {response.text}")
        return
    institution_id = response.json()["id"]
    print(f"   Institution created: {institution_id}")
    
    # 2. Create Job Group
    print("\n2. Creating Job Group...")
    group_code = f"JG_{generate_uuid()[:8]}"
    group_payload = {
        "institution_id": institution_id,
        "code": group_code,
        "name": "Test Job Group"
    }
    response = client.post("/organization/groups", json=group_payload)
    if response.status_code != 200:
        print(f"   Failed to create job group: {response.text}")
        return
    group_id = response.json()["id"]
    print(f"   Job Group created: {group_id}")
    
    # 3. Create Job Series
    print("\n3. Creating Job Series...")
    series_code = f"JS_{generate_uuid()[:8]}"
    series_payload = {
        "job_group_id": group_id,
        "code": series_code,
        "name": "Test Job Series"
    }
    response = client.post("/organization/series", json=series_payload)
    if response.status_code != 200:
        print(f"   Failed to create job series: {response.text}")
        return
    series_id = response.json()["id"]
    print(f"   Job Series created: {series_id}")
    
    # 4. Create Job Position
    print("\n4. Creating Job Position...")
    pos_code = f"JP_{generate_uuid()[:8]}"
    pos_payload = {
        "job_series_id": series_id,
        "code": pos_code,
        "name": "Test Job Position",
        "description": "Test Description"
    }
    response = client.post("/organization/positions", json=pos_payload)
    if response.status_code != 200:
        print(f"   Failed to create job position: {response.text}")
        return
    position_id = response.json()["id"]
    print(f"   Job Position created: {position_id}")
    
    # 5. Create Job Task
    print("\n5. Creating Job Task...")
    task_code = f"JT_{generate_uuid()[:8]}"
    task_payload = {
        "job_position_id": position_id,
        "code": task_code,
        "name": "Test Job Task"
    }
    response = client.post("/tasks/job-tasks", json=task_payload)
    if response.status_code != 200:
        print(f"   Failed to create job task: {response.text}")
        return
    task_id = response.json()["id"]
    print(f"   Job Task created: {task_id}")
    
    # 6. Create Work Item
    print("\n6. Creating Work Item...")
    work_code = f"WI_{generate_uuid()[:8]}"
    work_payload = {
        "job_task_id": task_id,
        "code": work_code,
        "name": "Test Work Item",
        "frequency": "WEEKLY",
        "estimated_hours_per_occurrence": 2.0,
        "workload_amount": 104.0
    }
    response = client.post("/tasks/work-items", json=work_payload)
    if response.status_code != 200:
        print(f"   Failed to create work item: {response.text}")
        return
    work_id = response.json()["id"]
    print(f"   Work Item created: {work_id}")
    
    # 7. Verify Hierarchy Retrieval
    print("\n7. Verifying Hierarchy Retrieval...")
    response = client.get(f"/organization/groups/{institution_id}")
    groups = response.json()
    if len(groups) > 0 and groups[-1]["id"] == group_id:
        print("   SUCCESS: Job Group retrieved.")
    else:
        print("   FAILURE: Job Group not retrieved.")
        
    response = client.get(f"/tasks/job-tasks/{position_id}")
    tasks = response.json()
    if len(tasks) > 0 and tasks[-1]["id"] == task_id:
        print("   SUCCESS: Job Task retrieved.")
    else:
        print("   FAILURE: Job Task not retrieved.")
        
    print("\nVerification Complete.")

if __name__ == "__main__":
    verify_organization_api()
