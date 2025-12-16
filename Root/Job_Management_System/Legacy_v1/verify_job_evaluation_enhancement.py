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

def verify_job_evaluation():
    db = SessionLocal()
    try:
        print("Starting Job Evaluation Enhancement Verification...")

        # 1. Create Institution
        inst = db.query(models.Institution).first()
        if not inst:
            inst = crud.create_institution(db, schemas.InstitutionCreate(name="Test Inst", code="TEST_JE"))

        # 2. Create Evaluation Factor
        factor = models.EvaluationFactor(
            institution_id=inst.id,
            name="Problem Solving",
            weight=0.3,
            description="Ability to solve complex problems"
        )
        db.add(factor)
        db.commit()
        db.refresh(factor)
        print(f"Created Evaluation Factor: {factor.name}")

        # 3. Create Point Table
        pt_data = schemas.PointTableCreate(
            factor_id=factor.id,
            level=1,
            score=20,
            criteria="Routine problems"
        )
        pt = crud.create_point_table(db, pt_data)
        print(f"Created Point Table: Level {pt.level} = {pt.score}")

        # 4. Create Job Evaluation Result
        # Need Job
        job = db.query(models.Job).first()
        if not job:
            # Need Department
            dept = db.query(models.Department).first()
            if not dept:
                dept = models.Department(name="Test Dept", code="DEPT_JE", institution_id=inst.id)
                db.add(dept)
                db.commit()
                db.refresh(dept)
            
            job_data = schemas.JobCreate(
                title="Evaluated Job", 
                department_id=dept.id
            )
            job = crud.create_job(db, job_data, institution_id=inst.id)

        result_data = schemas.JobEvaluationResultCreate(
            job_id=job.id,
            total_score=60.0,
            grade="G3"
        )
        result = crud.create_job_evaluation_result(db, result_data)
        print(f"Created Job Evaluation Result: Score {result.total_score}, Grade {result.grade}")

        # 5. Verify Retrieval
        fetched_result = crud.get_job_evaluation_result(db, job.id)
        assert fetched_result.total_score == 60.0
        print("Verified Result Retrieval.")

    except Exception as e:
        print(f"Verification Failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_job_evaluation()
