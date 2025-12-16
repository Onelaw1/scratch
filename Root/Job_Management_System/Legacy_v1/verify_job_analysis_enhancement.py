import sys
import os
from sqlalchemy.orm import Session

# Add Job Management System root to path
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

from backend.database import Base, engine, SessionLocal
from backend import models, schemas, crud

# Create tables
Base.metadata.create_all(bind=engine)

def verify_job_analysis():
    db = SessionLocal()
    try:
        print("Starting Job Analysis Enhancement Verification...")

        # 1. Create Action Verb
        verb_data = schemas.ActionVerbCreate(verb="Analyze", definition="To examine in detail")
        # Check if exists
        existing_verb = db.query(models.ActionVerb).filter(models.ActionVerb.verb == "Analyze").first()
        if not existing_verb:
            verb = crud.create_action_verb(db, verb_data)
            print(f"Created Action Verb: {verb.verb}")
        else:
            verb = existing_verb
            print(f"Using existing Action Verb: {verb.verb}")

        # 2. Create Task Dictionary Item
        task_dict_data = schemas.TaskDictionaryCreate(
            task_name="Analyze Financial Data",
            action_verb_id=verb.id,
            standard_time=2.5
        )
        task_item = crud.create_task_dictionary_item(db, task_dict_data)
        print(f"Created Task Dictionary Item: {task_item.task_name}")

        # 3. Create Job for Rule of 30 Test
        # Need Institution first
        inst = db.query(models.Institution).first()
        if not inst:
            inst = crud.create_institution(db, schemas.InstitutionCreate(name="Test Inst", code="TEST_JA"))
        
        # Need Department
        dept = db.query(models.Department).first()
        if not dept:
            dept = models.Department(name="Test Dept", code="DEPT01", institution_id=inst.id)
            db.add(dept)
            db.commit()
            db.refresh(dept)

        job_data = schemas.JobCreate(
            title="Test Analyst", 
            job_group_id="JG001", 
            job_series_id="JS001", 
            job_position_id="JP001",
            department_id=dept.id
        )
        
        job = crud.create_job(db, job_data, institution_id=inst.id)
        print(f"Created Job: {job.title}")

        # 4. Test Rule of 30
        print("Testing Rule of 30...")
        for i in range(30):
            task_data = schemas.JobTaskCreate(
                task_name=f"Task {i+1}",
                frequency="Daily",
                difficulty=3,
                importance=5
            )
            crud.create_job_task(db, task_data, job.id)
        
        print("Created 30 tasks successfully.")

        # 5. Try 31st task
        try:
            task_data = schemas.JobTaskCreate(
                task_name="Task 31",
                frequency="Daily",
                difficulty=3,
                importance=5
            )
            crud.create_job_task(db, task_data, job.id)
            print("ERROR: Rule of 30 failed! Created 31st task.")
        except ValueError as e:
            print(f"SUCCESS: Rule of 30 caught error: {e}")

    except Exception as e:
        print(f"Verification Failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_job_analysis()
