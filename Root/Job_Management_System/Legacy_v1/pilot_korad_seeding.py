import os
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, User, Institution, OrgUnit, PerformanceReview, JobPosition, JobTask, PositionGrade
from backend.services.nine_box_service import NineBoxService
from backend.services.span_service import SpanService

# Use the main DB for the pilot (be careful, this will add data to sql_app.db)
# To be safe, let's use a separate pilot DB that the user can switch to if they want,
# OR just add to the existing DB if it's empty. Use 'pilot_korad.db' for safety.
DB_URL = "sqlite:///./sql_app.db" # Using main DB for direct visibility
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def seed_korad_pilot():
    db = SessionLocal()
    try:
        print("🚀 Starting KORAD Pilot Data Seeding...")
        
        # 0. Cleanup (Optional: Be careful clearing prod DB)
        # For this demo, let's assume we append or the user has a fresh DB.
        # If specific users exist, skip.
        if db.query(Institution).filter_by(code="KORAD").first():
            print("⚠️ KORAD data might already exist. Skipping creation to avoid dups.")
            # return

        # 1. Institution
        inst = Institution(name="한국원자력환경공단", code="KORAD")
        db.add(inst)
        db.commit()

        # 2. Org Units Structure (Based on 2024 Info)
        # Hierarchy: 이사장 -> (부이사장) -> 본부 -> 실 -> 팀
        
        units = {}
        
        # Top Level
        units["CEO"] = OrgUnit(name="이사장실", unit_type="OFFICE", institution=inst)
        units["AUDIT"] = OrgUnit(name="감사실", unit_type="OFFICE", institution=inst)
        units["V_CEO"] = OrgUnit(name="부이사장", unit_type="OFFICE", institution=inst)
        
        # Direct under CEO
        units["QUAL_SAFE"] = OrgUnit(name="품질안전단", unit_type="DIVISION", institution=inst)
        units["COMM"] = OrgUnit(name="소통협력단", unit_type="DIVISION", institution=inst)
        
        # Headquarters (Under Vice CEO usually, but flat for now)
        units["LOW_RAD_HQ"] = OrgUnit(name="중저준위사업본부", unit_type="HQ", institution=inst)
        units["HIGH_RAD_HQ"] = OrgUnit(name="고준위사업본부", unit_type="HQ", institution=inst)
        units["FUND"] = OrgUnit(name="기금관리센터", unit_type="HQ", institution=inst) # Treated as HQ level
        
        # Rooms (Sil) & Teams
        # 중저준위
        units["LOW_PLAN_ROOM"] = OrgUnit(name="중저준위기획실", unit_type="DEPT", institution=inst, parent=units["LOW_RAD_HQ"])
        units["LOW_OP_ROOM"] = OrgUnit(name="중저준위운영실", unit_type="DEPT", institution=inst, parent=units["LOW_RAD_HQ"])
        units["LOW_SAFE_ROOM"] = OrgUnit(name="중저준위안전실", unit_type="DEPT", institution=inst, parent=units["LOW_RAD_HQ"])
        
        # 고준위
        units["HIGH_PLAN_ROOM"] = OrgUnit(name="고준위기획실", unit_type="DEPT", institution=inst, parent=units["HIGH_RAD_HQ"])
        units["HIGH_DEV_INST"] = OrgUnit(name="고준위기술개발원", unit_type="DEPT", institution=inst, parent=units["HIGH_RAD_HQ"])
        units["HR_DEV"] = OrgUnit(name="인력개발원", unit_type="DEPT", institution=inst, parent=units["HIGH_RAD_HQ"])

        db.add_all(units.values())
        db.commit()
        
        # 3. Job Positions & Grades
        grades = ["G1", "G2", "G3", "G4", "G5"] # G1=Executive, G5=Staff
        pos_templates = ["General Manager", "Senior Manager", "Manager", "Assistant Manager", "Staff"]
        
        # 4. Users (Employees) Generation
        # Strategy:
        # CEO -> Heads of HQs -> Heads of Rooms -> Team Leaders -> Members
        
        employees = []
        
        # 4.1 CEO
        ceo = User(email="ceo@korad.or.kr", name="조성돈", institution=inst, org_unit=units["CEO"], position_grade="Executive")
        db.add(ceo)
        db.commit() # Need ID

        # 4.2 HQ Heads (Direct Report to CEO)
        hq_heads = []
        hq_map = {
            "LOW_RAD_HQ": "오성훈", # Virtual Name
            "HIGH_RAD_HQ": "김민수",
            "QUAL_SAFE": "박정우",
            "COMM": "최영희",
            "FUND": "이동현"
        }
        
        for key, name in hq_map.items():
            u = User(email=f"{key.lower()}@korad.or.kr", name=name, institution=inst, org_unit=units[key], 
                     reports_to_id=ceo.id, position_grade="Director")
            hq_heads.append(u)
            employees.append(u)
        
        db.add_all(hq_heads)
        db.commit()

        # 4.3 Room Heads (Report to HQ Heads)
        # Low Rad HQ Structure
        low_hq_head = next(u for u in hq_heads if u.org_unit.name == "중저준위사업본부")
        
        room_heads = []
        # Create Room Heads for Low HQ
        for room_key, room_name, head_name in [
            ("LOW_PLAN_ROOM", "중저준위기획실장", "정기획"),
            ("LOW_OP_ROOM", "중저준위운영실장", "강운영"),
            ("LOW_SAFE_ROOM", "중저준위안전실장", "안재석")
        ]:
            u = User(email=f"{room_key.lower()}@korad.or.kr", name=head_name, institution=inst, org_unit=units[room_key],
                     reports_to_id=low_hq_head.id, position_grade="Senior Manager")
            room_heads.append(u)
            employees.append(u)

        db.add_all(room_heads)
        db.commit()

        # 4.4 Team Members (Mass Generation for Analytics)
        # Scenario 1: '중저준위운영실' has MANY members (Wide Span for '강운영')
        op_room_head = next(u for u in room_heads if u.name == "강운영")
        
        # Generate 18 members for this room head (Bottleneck)
        for i in range(18):
            # Mix 9-Box Profiles
            # Good Performers
            perf = random.randint(70, 95)
            pot = random.randint(60, 95)
            
            # Scenario: Some risk employee
            if i % 10 == 0: 
                perf = 40; pot = 40; # Risk
            # Scenario: High Potential
            elif i % 5 == 0:
                perf = 85; pot = 92; # High Pot

            u = User(
                email=f"op_staff_{i}@korad.or.kr", 
                name=f"운영팀원_{i+1}", 
                institution=inst, 
                org_unit=units["LOW_OP_ROOM"],
                reports_to_id=op_room_head.id,
                position_grade=random.choice(["Manager", "Assistant", "Staff"])
            )
            db.add(u)
            db.commit()
            
            # Create Review
            rev = PerformanceReview(
                user_id=u.id, year=2024, status="FINAL",
                total_score=perf, score_potential=pot
            )
            db.add(rev)

        # Scenario 2: '중저준위기획실' has FEW members (Narrow Span)
        plan_room_head = next(u for u in room_heads if u.name == "정기획")
        
        for i in range(2): # Only 2 members
            u = User(
                email=f"plan_staff_{i}@korad.or.kr", 
                name=f"기획담당_{i+1}", 
                institution=inst, 
                org_unit=units["LOW_PLAN_ROOM"],
                reports_to_id=plan_room_head.id,
                position_grade="Manager"
            )
            db.add(u)
            db.commit()
            
            # High Performers
            rev = PerformanceReview(
                user_id=u.id, year=2024, status="FINAL",
                total_score=92, score_potential=88
            )
            db.add(rev)

        # Scenario 3: Executive 9-Box
        # HQ Heads usually are High Performers, but let's make one Enigma
        for hq in hq_heads:
            if hq.name == "최영희": # 소통협력단
                perf = 75; pot = 90 # Enigma
            else:
                perf = 88; pot = 85 # Core/High Perf
            
            rev = PerformanceReview(
                user_id=hq.id, year=2024, status="FINAL",
                total_score=perf, score_potential=pot
            )
            db.add(rev)

        db.commit()

        print("✅ Data Seeding Completed.")
        print("- Institution: KORAD Created")
        print("- Org Structure: HQ > Rooms created")
        print("- Users: 30+ users created with hierarchy")
        print("- Performance Reviews: Created for 9-Box grid")
        
        # 6. Competency Seeding (NCS Based)
        print("Seeding Competency Data...")
        from backend.models import Competency, JobCompetency, UserCompetency
        
        # Define some core competencies for KORAD
        comp_list = [
            ("COMP_01", "Nuclear Safety", "Knowledge of safety regulations"),
            ("COMP_02", "Project Mgmt", "Ability to manage complex projects"),
            ("COMP_03", "Communication", "Internal/External stakeholder comms"),
            ("COMP_04", "Data Analysis", "Statistical analysis skills"),
            ("COMP_05", "Leadership", "Team leading and mentoring")
        ]
        
        competencies = {}
        for code, name, desc in comp_list:
            c = Competency(name=name, description=desc, category="Core")
            db.add(c)
            db.commit() # Get ID
            competencies[name] = c
            
        # Define Job Requirements (Simplification: All managers need Leadership 3, PM 3)
        # Create a generic 'Manager' position for linkage if not exists
        mgr_pos = JobPosition(title="Manager", code="POS_MGR", department_id=units["LOW_OP_ROOM"].id)
        db.add(mgr_pos)
        db.commit()
        
        # Link reqs
        db.add(JobCompetency(job_position_id=mgr_pos.id, competency_id=competencies["Leadership"].id, required_level=3))
        db.add(JobCompetency(job_position_id=mgr_pos.id, competency_id=competencies["Project Mgmt"].id, required_level=4))
        db.add(JobCompetency(job_position_id=mgr_pos.id, competency_id=competencies["Communication"].id, required_level=3))
        db.commit()
        
        # Assign this position to some users (e.g., '강운영')
        op_room_head = next(u for u in room_heads if u.name == "강운영")
        op_room_head.job_positions.append(mgr_pos)
        
        # Assign Actual Skills to '강운영' (Gap Scenario)
        # Leadership: 2 (Gap -1), PM: 5 (Surplus +1), Comm: 3 (Match)
        db.add(UserCompetency(user_id=op_room_head.id, competency_id=competencies["Leadership"].id, current_level=2))
        db.add(UserCompetency(user_id=op_room_head.id, competency_id=competencies["Project Mgmt"].id, current_level=5))
        db.add(UserCompetency(user_id=op_room_head.id, competency_id=competencies["Communication"].id, current_level=3))
        
        db.commit()
        print("✅ Competency Data Seeded.")

        # 5. Run Analytics Services to pre-calculate
        print("Running Analytics...")
        NineBoxService(db).generate_grid_data()
        SpanService(db).analyze_org_structure()
        print("✅ Analytics Updated.")

    except Exception as e:
        print(f"❌ Seeding Failed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_korad_pilot()
