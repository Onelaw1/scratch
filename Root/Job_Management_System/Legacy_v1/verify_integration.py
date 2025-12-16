from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import (
    Base, User, Institution, OrgUnit, JobGroup, JobSeries, JobPosition, 
    Competency, JobCompetency, UserCompetency, PerformanceReview
)
from backend.services.nine_box_service import NineBoxService
from backend.services.span_service import SpanService
from backend.services.competency_service import CompetencyService
import os
import uuid
import datetime

# Setup test DB
TEST_DB_URL = "sqlite:///./test_integration.db"
if os.path.exists("./test_integration.db"):
    os.remove("./test_integration.db")

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def verify_integration():
    db = SessionLocal()
    try:
        print("=== 1. Setting up Org Structure ===")
        inst = Institution(name="Global Corp", code="GC001", id=str(uuid.uuid4()))
        unit = OrgUnit(name="HQ", unit_type="HQ", institution=inst, id=str(uuid.uuid4()))
        db.add_all([inst, unit])
        db.commit()
        
        print("=== 2. Setting up Job Architecture & Competencies ===")
        # Competencies
        comp_python = Competency(name="Python", category="Tech", id=str(uuid.uuid4()))
        comp_comm = Competency(name="Communication", category="Soft", id=str(uuid.uuid4()))
        db.add_all([comp_python, comp_comm])
        
        # Job
        grp = JobGroup(name="Tech", id=str(uuid.uuid4()))
        series = JobSeries(name="Dev", group=grp, id=str(uuid.uuid4()))
        db.add_all([grp, series])
        db.commit()
        
        # Position (Senior Dev)
        pos_senior = JobPosition(title="Senior Dev", series=series, id=str(uuid.uuid4()))
        db.add(pos_senior)
        db.commit()
        
        # Job Requirements (Python: 5, Communication: 4)
        jc1 = JobCompetency(job_position_id=pos_senior.id, competency_id=comp_python.id, required_level=5)
        jc2 = JobCompetency(job_position_id=pos_senior.id, competency_id=comp_comm.id, required_level=4)
        db.add_all([jc1, jc2])
        db.commit()
        
        print("=== 3. Hiring & Reporting Lines ===")
        # CEO -> Head -> Senior Dev
        ceo = User(name="CEO", email="ceo@gc.com", institution=inst, org_unit=unit, id=str(uuid.uuid4()))
        db.add(ceo)
        db.commit()
        
        head = User(name="Head of Eng", email="head@gc.com", institution=inst, org_unit=unit, reports_to_id=ceo.id, id=str(uuid.uuid4()))
        db.add(head)
        db.commit()
        
        # Employee (Subject)
        emp = User(name="Alice", email="alice@gc.com", institution=inst, org_unit=unit, reports_to_id=head.id, id=str(uuid.uuid4()))
        emp.job_positions.append(pos_senior) # Assign Job
        db.add(emp)
        db.commit()
        
        print("=== 4. Performance Review (9-Box Data) ===")
        # High Performer, High Potential -> Box 9 (Star)
        review = PerformanceReview(
            user_id=emp.id, 
            year=2024, 
            status="FINAL", 
            total_score=95.0, # High Perf
            score_potential=90.0, # High Pot
            id=str(uuid.uuid4())
        )
        db.add(review)
        db.commit()
        
        # Run 9-Box Service
        nine_service = NineBoxService(db)
        nine_result = nine_service.generate_grid_data()
        
        # Verify
        alice_data = next((e for e in nine_result['employees'] if e['name'] == "Alice"), None)
        print(f"9-Box Result: Box {alice_data['box']} ({alice_data['category']})")
        assert alice_data['box'] == 9
        assert alice_data['category'] == "Star"
        
        print("=== 5. Competency Evaluation (Radar) ===")
        # Alice is good at Python (5/5) but lacks comms (2/4)
        uc1 = UserCompetency(user_id=emp.id, competency_id=comp_python.id, current_level=5)
        uc2 = UserCompetency(user_id=emp.id, competency_id=comp_comm.id, current_level=2)
        db.add_all([uc1, uc2])
        db.commit()
        
        # Run Competency Service
        comp_service = CompetencyService(db)
        comp_result = comp_service.analyze_fit(emp.id)
        
        # Verify
        gaps = comp_result['analysis']['gaps']
        print(f"Competency Gaps: {[g['skill'] for g in gaps]}")
        assert len(gaps) == 1
        assert gaps[0]['skill'] == "Communication"
        
        print("=== 6. Organizational Analysis (Span of Control) ===")
        # Run Span Service
        span_service = SpanService(db)
        span_result = span_service.analyze_org_structure()
        
        # Verify Hierarchy
        head_node = next(n for n in span_result['nodes'] if n['name'] == "Head of Eng")
        print(f"Head Span: {head_node['span']} (Exp: 1 - Alice)")
        assert head_node['span'] == 1
        
        print("\n>>> INTEGRATION VERIFICATION SUCCESSFUL! <<<")

    except Exception as e:
        print(f"\n>>> VERIFICATION FAILED: {e} <<<")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        if os.path.exists("./test_integration.db"):
            try:
                os.remove("./test_integration.db")
            except:
                pass

if __name__ == "__main__":
    verify_integration()
