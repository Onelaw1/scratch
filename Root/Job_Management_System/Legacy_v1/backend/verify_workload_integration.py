import sys
import os
import uuid
from fastapi.testclient import TestClient

# Add Root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Report_Analysis_Project")))

from backend.main import app

client = TestClient(app)

def generate_uuid():
    return str(uuid.uuid4())

def verify_workload_integration():
    print("Starting Workload Survey Integration Verification (TestClient)...")

    # 1. Setup: Create Job Hierarchy
    print("\n1. Setting up test data...")
    
    job_data = [
        {
            "id": generate_uuid(),
            "code": "JS_TEST_TC",
            "name": "Test Job Series TC",
            "positions": [
                {
                    "id": generate_uuid(),
                    "code": "JP_TEST_TC",
                    "name": "Test Job Position TC",
                    "tasks": [
                        {
                            "id": generate_uuid(),
                            "category": "Test Category",
                            "name": "Test Task TC",
                            "workItems": [
                                {
                                    "id": generate_uuid(),
                                    "code": "WI_TEST_TC",
                                    "name": "Test Work Item TC",
                                    "frequency": "MONTHLY",
                                    "time": 2.0,
                                    "count": 12,
                                    "workload": 24.0
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
    
    print("   Updating classification matrix...")
    response = client.post("/job-centric/classification/matrix", json=job_data)
    if response.status_code != 200:
        print(f"   Failed to update classification matrix: {response.text}")
        return
    print("   Classification matrix updated.")
    
    position_id = job_data[0]["positions"][0]["id"]
    work_item_id = job_data[0]["positions"][0]["tasks"][0]["workItems"][0]["id"]
    
    # Fetch users to pick one
    print("   Fetching users...")
    response = client.get("/job-centric/workload/survey")
    if response.status_code != 200:
        print(f"   Failed to fetch users: {response.text}")
        return
    
    users = response.json()
    if not users:
        print("   No users found. Cannot proceed.")
        return
    
    test_user = users[0]
    print(f"   Using user: {test_user['name']} ({test_user['id']})")
    
    # Assign user to position
    print(f"   Assigning user {test_user['id']} to position {position_id}...")
    response = client.post(f"/job-centric/users/{test_user['id']}/assign-position/{position_id}")
    if response.status_code != 200:
        print(f"   Failed to assign user to position: {response.text}")
        return
    print("   User assigned to position.")
    
    # 2. Verify: Get Workload Survey
    print("\n2. Verifying GET /workload/survey...")
    response = client.get("/job-centric/workload/survey")
    users = response.json()
    target_user = next((u for u in users if u['id'] == test_user['id']), None)
    
    if not target_user:
        print("   Target user not found.")
        return
        
    found_task = next((t for t in target_user['tasks'] if t['id'] == work_item_id), None)
    
    if found_task:
        print(f"   SUCCESS: Found standard task linked to WorkItem {work_item_id}")
    else:
        print(f"   FAILURE: Standard task linked to WorkItem {work_item_id} NOT found.")
        return

    # 3. Verify: Post Workload Survey
    print("\n3. Verifying POST /workload/survey...")
    payload = {
        "id": target_user['id'],
        "name": target_user['name'],
        "department": target_user['department'],
        "tasks": [
            {
                "id": work_item_id,
                "name": "Ignored",
                "frequency": "Ignored",
                "hoursPerOccurrence": 0,
                "totalHours": 100.0
            }
        ],
        "totalHours": 100.0
    }
    
    response = client.post(f"/job-centric/workload/survey/{target_user['id']}", json=payload)
    if response.status_code != 200:
        print(f"   Failed to submit survey: {response.text}")
        return
        
    result = response.json()
    updated_task = next((t for t in result['tasks'] if t['id'] == work_item_id), None)
    if updated_task and updated_task['totalHours'] == 100.0:
        print("   SUCCESS: Response reflects updated hours.")
    else:
        print("   FAILURE: Response does not reflect updated hours.")
        return
        
    # 4. Verify Persistence
    print("\n4. Verifying Persistence...")
    response = client.get("/job-centric/workload/survey")
    users = response.json()
    target_user = next((u for u in users if u['id'] == test_user['id']), None)
    saved_task = next((t for t in target_user['tasks'] if t['id'] == work_item_id), None)
    
    if saved_task and saved_task['totalHours'] == 100.0:
        print("   SUCCESS: Data persisted correctly.")
    else:
        print("   FAILURE: Data did not persist.")
        
    print("\nVerification Complete.")

if __name__ == "__main__":
    verify_workload_integration()
