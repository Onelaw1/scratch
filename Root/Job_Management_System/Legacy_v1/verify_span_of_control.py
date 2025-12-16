from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, User, Institution
from backend.services.span_service import SpanService
import os

# Setup test DB
TEST_DB_URL = "sqlite:///./test_span.db"
if os.path.exists("./test_span.db"):
    os.remove("./test_span.db")

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def verify_span():
    db = SessionLocal()
    try:
        print("Setting up test data...")
        
        inst = Institution(name="Test Inst", code="SPAN001")
        db.add(inst)
        db.commit()

        # Hierarchy:
        # CEO (Reports: 2)
        #  |- VP1 (Reports: 3 -> Optimal/Narrow)
        #  |   |- Mgr1 (Reports: 1 -> Narrow)
        #  |   |   |- Staff1
        #  |   |- Mgr2 (Reports: 0 -> IC)
        #  |   |- Mgr3 (Reports: 20 -> Wide)
        #  |       |- Staff... (x20)
        #  |- VP2 (Reports: 0 -> IC)

        # 1. Create Nodes
        ceo = User(email="ceo@test.com", name="CEO", institution=inst)
        vp1 = User(email="vp1@test.com", name="VP 1", institution=inst)
        vp2 = User(email="vp2@test.com", name="VP 2", institution=inst)
        
        mgr1 = User(email="mgr1@test.com", name="Mgr 1", institution=inst)
        mgr2 = User(email="mgr2@test.com", name="Mgr 2", institution=inst)
        mgr3 = User(email="mgr3@test.com", name="Mgr 3 (Wide)", institution=inst)
        
        staff1 = User(email="s1@test.com", name="Staff 1", institution=inst)
        
        db.add_all([ceo, vp1, vp2, mgr1, mgr2, mgr3, staff1])
        db.commit() # Get IDs

        # 2. Build Relations
        vp1.reports_to_id = ceo.id
        vp2.reports_to_id = ceo.id
        
        mgr1.reports_to_id = vp1.id
        mgr2.reports_to_id = vp1.id
        mgr3.reports_to_id = vp1.id
        
        staff1.reports_to_id = mgr1.id
        
        # Add mass reports to Mgr 3
        mass_reports = []
        for i in range(20):
            u = User(email=f"m3_s{i}@test.com", name=f"M3 Staff {i}", institution=inst, reports_to_id=mgr3.id)
            mass_reports.append(u)
        db.add_all(mass_reports)
        
        db.commit()

        print("Running SpanService...")
        service = SpanService(db)
        result = service.analyze_org_structure()
        
        metrics = result['metrics']
        print(f"Metrics: {metrics}")
        
        # Verify
        # CEO Span: 2 (VP1, VP2)
        ceo_node = next(n for n in result['nodes'] if n['name'] == "CEO")
        print(f"CEO Span: {ceo_node['span']} (Expected 2)")
        assert ceo_node['span'] == 2
        
        # Mgr3 Span: 20 -> Wide Alert
        m3_node = next(n for n in result['nodes'] if n['name'] == "Mgr 3 (Wide)")
        print(f"Mgr3 Span: {m3_node['span']} (Expected 20)")
        assert m3_node['span'] == 20
        assert "Wide" in m3_node['status']
        
        # Check Alert Existence
        alert_names = [a['name'] for a in result['alerts']]
        assert "Mgr 3 (Wide)" in alert_names
        print("Alert verified for Mgr 3")

        print("VERIFICATION SUCCESSFUL!")

    except Exception as e:
        print(f"VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        if os.path.exists("./test_span.db"):
            try:
                os.remove("./test_span.db")
            except:
                pass

if __name__ == "__main__":
    verify_span()
