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

def verify_job_classification():
    db = SessionLocal()
    try:
        print("Starting Job Classification Enhancement Verification...")

        # 1. Create Hierarchy (Group -> Series -> Position)
        # Need Institution
        inst = db.query(models.Institution).first()
        if not inst:
            inst = crud.create_institution(db, schemas.InstitutionCreate(name="Test Inst", code="TEST_JC"))

        # Create Job Group
        group = models.JobGroup(code="JG02", name="Management", institution_id=inst.id)
        db.add(group)
        db.commit()
        db.refresh(group)
        print(f"Created Job Group: {group.name}")

        # Create Job Series
        series = models.JobSeries(code="JS02", name="HR", job_group_id=group.id)
        db.add(series)
        db.commit()
        db.refresh(series)
        print(f"Created Job Series: {series.name}")

        # Create Job Position
        position = models.JobPosition(code="JP02", name="Recruiter", job_series_id=series.id)
        db.add(position)
        db.commit()
        db.refresh(position)
        print(f"Created Job Position: {position.name}")

        # 2. Create NCS Mapping
        ncs_data = schemas.NCSMappingCreate(
            job_position_id=position.id,
            ncs_code="02020201",
            ncs_name="Recruitment Planning",
            ncs_level=5
        )
        mapping = crud.create_ncs_mapping(db, ncs_data)
        print(f"Created NCS Mapping: {mapping.ncs_code} - {mapping.ncs_name}")

        # 3. Verify Mapping
        mappings = crud.get_ncs_mappings(db, position.id)
        assert len(mappings) > 0
        assert mappings[0].ncs_code == "02020201"
        print("Verified NCS Mapping retrieval.")

    except Exception as e:
        print(f"Verification Failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_job_classification()
