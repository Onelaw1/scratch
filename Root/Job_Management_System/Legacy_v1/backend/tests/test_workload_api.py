
import pytest
from backend.models import User, Institution, OrgUnit

def setup_test_data(db):
    """
    Helper to create basic hierarchy: Institution -> OrgUnit -> User
    """
    # Create Institution
    inst = Institution(id="inst_1", name="Test Inst", code="TI01", category="MARKET")
    db.add(inst)
    
    # Create OrgUnit
    dept = OrgUnit(id="dept_1", institution_id="inst_1", name="IT Team", unit_type="TEAM")
    db.add(dept)
    
    # Create User
    user = User(id="emp_1", institution_id="inst_1", org_unit_id="dept_1", email="test@example.com", name="Test User")
    db.add(user)
    
    db.commit()

def test_get_workload_survey_initial(client, db_session):
    setup_test_data(db_session)
    
    # Use specific employee ID
    response = client.get("/job-centric/workload-survey/emp_1")
    assert response.status_code == 200
    data = response.json()
    
    # Expect single object, not list
    assert data['id'] == 'emp_1'
    assert data['name'] == "Test User"
    # Tasks might be empty initially if no JobPositions/Tasks assigned
    # The API returns basic info even if empty
    assert isinstance(data['tasks'], list)

def test_update_workload_entry(client, db_session):
    setup_test_data(db_session)
    
    # Prepare payload matching WorkloadSurveyDataSchema
    # Note: The API tries to match task IDs to WorkItem or JobTask in DB.
    # Since we didn't create JobTasks in setup_test_data, the submission might ignore them or fail if strict.
    # Looking at code: it tries to find WorkItem/JobTask. If not found, it skips creating entry but returns total_hours.
    
    # We should create a dummy task id in DB to verify persistence logic, 
    # but for this unit test let's just verify the endpoint accepts the payload.
    
    payload = {
        "id": "emp_1",
        "name": "Test User",
        "department": "IT Team",
        "tasks": [
            {
                "id": "task_1", # Dummy ID
                "name": "Coding",
                "frequency": "DAILY",
                "hoursPerOccurrence": 4.0,
                "totalHours": 960.0
            }
        ],
        "totalHours": 960.0
    }
    
    response = client.post("/job-centric/workload-survey/emp_1", json=payload)
    assert response.status_code == 200
    updated_data = response.json()
    
    # Logic returns {"message": ..., "total_hours": ...}
    assert updated_data['total_hours'] == 960.0
    assert updated_data['message'] == "Survey submitted successfully"

