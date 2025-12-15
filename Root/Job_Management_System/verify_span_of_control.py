from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, User, Institution, OrgUnit
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
        print("Setting up hierarchy...")
        
        # 1. Inst & Unit
        inst = Institution(name="Test Inst", code="T01")
        unit = OrgUnit(name="HQ", unit_type="HQ", institution=inst)
        db.add(inst)
        db.add(unit)
        db.commit()
        
        # 2. Hierarchy: CEO -> Mgr1 -> [Staff1, Staff2]
        ceo = User(email="ceo@test.com", name="CEO", institution=inst, org_unit=unit)
        db.add(ceo)
        db.commit() # ID gen
        
        mgr = User(email="mgr@test.com", name="Manager", institution=inst, org_unit=unit, reports_to_id=ceo.id)
        db.add(mgr)
        db.commit()
        
        s1 = User(email="s1@test.com", name="Staff1", institution=inst, org_unit=unit, reports_to_id=mgr.id)
        s2 = User(email="s2@test.com", name="Staff2", institution=inst, org_unit=unit, reports_to_id=mgr.id)
        s3 = User(email="s3@test.com", name="Staff3", institution=inst, org_unit=unit, reports_to_id=mgr.id)
        db.add_all([s1, s2, s3])
        db.commit()
        
        # Refresh relationships
        db.refresh(ceo)
        db.refresh(mgr)
        
        print("Running SpanService...")
        service = SpanService(db)
        result = service.analyze_org_structure()
        
        metrics = result['metrics']
        print(f"Metrics: {metrics}")
        
        # Verify CEO Span (1: Manager)
        ceo_node = next(n for n in result['nodes'] if n['name'] == "CEO")
        print(f"CEO Span: {ceo_node['span']} (Exp: 1)")
        assert ceo_node['span'] == 1
        
        # Verify Mgr Span (3: Staff)
        mgr_node = next(n for n in result['nodes'] if n['name'] == "Manager")
        print(f"Mgr Span: {mgr_node['span']} (Exp: 3)")
        assert mgr_node['span'] == 3
        
        # Verify Depth
        print(f"Max Layers: {metrics['max_layers']} (Exp: 3)")
        assert metrics['max_layers'] == 3
        
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
