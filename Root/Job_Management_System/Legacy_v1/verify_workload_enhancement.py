import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime

# Add Job Management System root to path
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

from backend.database import Base, engine, SessionLocal
from backend import models, schemas, crud

# Create tables
Base.metadata.create_all(bind=engine)

def verify_workload_enhancement():
    db = SessionLocal()
    try:
        print("Starting Workload Analysis Enhancement Verification...")

        # 1. Create Survey Period
        # Need Institution
        inst = db.query(models.Institution).first()
        if not inst:
            inst = crud.create_institution(db, schemas.InstitutionCreate(name="Test Inst", code="TEST_WA"))
        
        survey_data = schemas.SurveyPeriodCreate(
            name="2024 Workload Survey",
            start_date=datetime.now(),
            end_date=datetime.now(),
            status="DRAFT"
        )
        survey = crud.create_survey_period(db, survey_data, inst.id)
        print(f"Created Survey Period: {survey.name}")

        # Need Department
        dept = db.query(models.Department).first()
        if not dept:
            dept = models.Department(name="Test Dept", code="DEPT_WA", institution_id=inst.id)
            db.add(dept)
            db.commit()
            db.refresh(dept)

        # 2. Create User
        user = db.query(models.User).first()
        if not user:
            user = models.User(
                name="Test User", 
                email="test@example.com", 
                institution_id=inst.id,
                department_id=dept.id
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # 3. Create Workload Entry with FTE params
        entry_data = schemas.WorkloadEntryCreate(
            survey_period_id=survey.id,
            user_id=user.id,
            actual_hours_per_year=200, # Legacy field
            perceived_workload=3,
            standard_time=2.0,
            volume=100.0
        )
        
        entry = crud.create_workload_entry(db, entry_data)
        print(f"Created Workload Entry. Standard Time: {entry.standard_time}, Volume: {entry.volume}")
        
        # 4. Verify FTE Calculation
        expected_fte = (2.0 * 100.0) / 1920.0
        print(f"Expected FTE: {expected_fte}")
        print(f"Actual FTE: {entry.fte_value}")
        
        assert abs(entry.fte_value - expected_fte) < 0.0001
        print("SUCCESS: FTE Calculation Verified.")

    except Exception as e:
        print(f"Verification Failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_workload_enhancement()
