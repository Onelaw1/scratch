import sys
import os
from uuid import uuid4
from datetime import date

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, engine
from backend.models import Base, EvaluationSession, EvaluationCriteria, JobPosition, JobSeries, JobGroup, Institution, SurveyStatus, InstitutionCategory

def seed_matrix_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        print("--- Seeding Matrix Demo Data ---")
        
        # 1. Ensure Institution (Force 'inst-001')
        TARGET_INST_ID = "inst-001"
        inst = db.query(Institution).filter(Institution.id == TARGET_INST_ID).first()
        if not inst:
            print(f"Creating Institution {TARGET_INST_ID}...")
            inst = Institution(id=TARGET_INST_ID, name="Demo Corp", code="DEMO_001", category=InstitutionCategory.MARKET)
            db.add(inst)
            db.commit()
        
        # 2. Create Session linked to inst-001
        session_id = str(uuid4())
        session = EvaluationSession(
            id=session_id,
            institution_id=TARGET_INST_ID,
            name="2024 Executive Evaluation (Demo)",
            start_date=date.today(),
            end_date=date.today(),
            status=SurveyStatus.ACTIVE
        )
        db.add(session)
        print(f"Created Session: {session.name} ({session.id})")
        
        # 3. Create Criteria
        criteria = [
            {"name": "Knowledge", "weight": 0.2, "category": "Expertise"},
            {"name": "Problem Solving", "weight": 0.3, "category": "Process"},
            {"name": "Impact", "weight": 0.3, "category": "Outcome"},
            {"name": "Communication", "weight": 0.2, "category": "Soft Skill"},
        ]
        
        for c in criteria:
            crit = EvaluationCriteria(
                id=str(uuid4()),
                session_id=session_id,
                name=c["name"],
                weight=c["weight"],
                category=c["category"]
            )
            db.add(crit)
        print(f"Added {len(criteria)} evaluation criteria.")

        # 4. Ensure Jobs (Check if we have enough jobs for a matrix)
        jobs_count = db.query(JobPosition).count()
        if jobs_count < 5:
            print("Adding more demo jobs...")
            # Ensure Group/Series exists
            group = db.query(JobGroup).first()
            if not group:
                group = JobGroup(id=str(uuid4()), name="Demo Group")
                db.add(group)
                db.commit() # Commit to get ID for series
                
            series = db.query(JobSeries).first()
            if not series:
                series = JobSeries(id=str(uuid4()), group_id=group.id, name="Demo Series")
                db.add(series)
                db.commit()

            new_jobs = ["Strategic Planning Lead", "IT Director", "HR Manager", "Senior Analyst", "Operations Head"]
            for title in new_jobs:
                job = JobPosition(
                    id=str(uuid4()),
                    series_id=series.id,
                    title=title,
                    grade="G3"
                )
                db.add(job)
            print(f"Added {len(new_jobs)} demo jobs.")
            
        db.commit()
        print("--- Seeding Complete ---")
        print(f"SESSION_ID: {session_id}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_matrix_data()
