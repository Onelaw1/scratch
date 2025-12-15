from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, User, PerformanceReview, Institution, OrgUnit
from backend.services.nine_box_service import NineBoxService
import os

# Setup test DB
TEST_DB_URL = "sqlite:///./test_nine_box.db"
if os.path.exists("./test_nine_box.db"):
    os.remove("./test_nine_box.db")

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def verify_nine_box():
    db = SessionLocal()
    try:
        print("Setting up test data...")
        
        # 1. Create Institution & Org Unit
        inst = Institution(name="Test Inst", code="TEST001")
        unit = OrgUnit(name="Test Team", unit_type="TEAM", institution=inst)
        db.add(inst)
        db.add(unit)
        db.commit()

        # 2. Create Users
        users = []
        # Case 1: Star (High Perf, High Pot)
        u1 = User(email="star@test.com", name="Star Player", institution=inst, org_unit=unit)
        # Case 2: Core (Mod Perf, Mod Pot)
        u2 = User(email="core@test.com", name="Core Player", institution=inst, org_unit=unit)
        # Case 3: Risk (Low Perf, Low Pot)
        u3 = User(email="risk@test.com", name="Risk Player", institution=inst, org_unit=unit)
        
        db.add_all([u1, u2, u3])
        db.commit()
        
        # 3. Create Reviews
        # Star: 90 Perf, 90 Pot -> Box 9
        r1 = PerformanceReview(
            user_id=u1.id, year=2024, status="FINAL",
            score_job=90, score_common=90, score_leadership=90,
            total_score=90, score_potential=90
        )
        # Core: 65 Perf, 65 Pot -> Box 5 (Mod/Mod)
        r2 = PerformanceReview(
            user_id=u2.id, year=2024, status="FINAL",
            score_job=65, score_common=65, score_leadership=65,
            total_score=65, score_potential=65
        )
        # Risk: 30 Perf, 30 Pot -> Box 1
        r3 = PerformanceReview(
            user_id=u3.id, year=2024, status="FINAL",
            score_job=30, score_common=30, score_leadership=30,
            total_score=30, score_potential=30
        )
        
        db.add_all([r1, r2, r3])
        db.commit()
        
        print("Running NineBoxService...")
        service = NineBoxService(db)
        result = service.generate_grid_data()
        
        print(f"Total Employees: {result['total_employees']}")
        
        # Verify
        employees = {e['id']: e for e in result['employees']}
        
        # Check Star
        star = employees[u1.id]
        print(f"Star: Box {star['box']} (Expected 9)")
        assert star['box'] == 9, f"Star should be Box 9, got {star['box']}"
        
        # Check Core
        core = employees[u2.id]
        print(f"Core: Box {core['box']} (Expected 5)")
        assert core['box'] == 5, f"Core should be Box 5, got {core['box']}"
        
        # Check Risk
        risk = employees[u3.id]
        print(f"Risk: Box {risk['box']} (Expected 1)")
        assert risk['box'] == 1, f"Risk should be Box 1, got {risk['box']}"
        
        print("VERIFICATION SUCCESSFUL!")
        
    except Exception as e:
        print(f"VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        if os.path.exists("./test_nine_box.db"):
            try:
                os.remove("./test_nine_box.db")
            except:
                pass

if __name__ == "__main__":
    verify_nine_box()
