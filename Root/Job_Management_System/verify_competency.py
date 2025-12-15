from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, User, JobPosition, JobSeries, JobGroup, Competency, JobCompetency, UserCompetency
from backend.services.competency_service import CompetencyService
import os
import uuid

# Setup test DB
TEST_DB_URL = "sqlite:///./test_competency.db"
if os.path.exists("./test_competency.db"):
    os.remove("./test_competency.db")

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def verify_competency():
    db = SessionLocal()
    try:
        print("Seeding Competency Data...")
        
        # 1. Job Architecture
        grp = JobGroup(name="Tech", id=str(uuid.uuid4()))
        series = JobSeries(name="Dev", group=grp, id=str(uuid.uuid4()))
        db.add_all([grp, series])
        db.commit()
        
        user = User(name="Test User", email="test@c.com", id=str(uuid.uuid4()))
        job = JobPosition(title="SRE", series=series, user=user, id=str(uuid.uuid4()))
        db.add_all([user, job])
        db.commit()
        
        # 2. Competencies
        c1 = Competency(name="Python", category="Tech", id=str(uuid.uuid4()))
        c2 = Competency(name="AWS", category="Tech", id=str(uuid.uuid4()))
        db.add_all([c1, c2])
        db.commit()
        
        # 3. Requirements (Standard)
        # Python: 4, AWS: 3
        jc1 = JobCompetency(job_position_id=job.id, competency_id=c1.id, required_level=4)
        jc2 = JobCompetency(job_position_id=job.id, competency_id=c2.id, required_level=3)
        db.add_all([jc1, jc2])
        db.commit()
        
        # 4. User Skills (Actual)
        # Python: 3 (Gap -1), AWS: 4 (Surplus +1)
        uc1 = UserCompetency(user_id=user.id, competency_id=c1.id, current_level=3)
        uc2 = UserCompetency(user_id=user.id, competency_id=c2.id, current_level=4)
        db.add_all([uc1, uc2])
        db.commit()
        
        # 5. Verify
        print("Running CompetencyService...")
        service = CompetencyService(db)
        result = service.analyze_fit(user.id)
        
        print(f"Fit Score: {result['fit_score']}")
        print(f"Radar Data: {result['radar_data']}")
        
        # Assertions
        radar = {r['skill']: r for r in result['radar_data']}
        
        # Python Check
        py_data = radar['Python']
        assert py_data['required'] == 4
        assert py_data['actual'] == 3
        print("Python Gap Verified.")
        
        # AWS Check
        aws_data = radar['AWS']
        assert aws_data['required'] == 3
        assert aws_data['actual'] == 4
        print("AWS Surplus Verified.")
        
        # Gaps List
        gaps = result['analysis']['gaps']
        assert len(gaps) == 1
        assert gaps[0]['skill'] == "Python"
        print("Gap Analysis Verified.")
        
        print("VERIFICATION SUCCESSFUL!")

    except Exception as e:
        print(f"VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        # Clean up
        if os.path.exists("./test_competency.db"):
            try:
                os.remove("./test_competency.db")
            except:
                pass

if __name__ == "__main__":
    verify_competency()
