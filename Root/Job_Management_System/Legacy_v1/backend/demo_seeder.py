
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add root to python path
sys.path.append(os.getcwd())

from backend.database import Base, SQLALCHEMY_DATABASE_URL
from backend import models

# Force use of sql_app.db if not set
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    # Ensure we use the file based db for persistence in demo
    db_path = os.path.join(os.getcwd(), "sql_app.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        print(f"Seeding database at {SQLALCHEMY_DATABASE_URL}")
        Base.metadata.create_all(bind=engine)
        
        # Check if data exists
        if not db.query(models.Institution).filter_by(id="inst_1").first():
            # 1. Institution
            inst = models.Institution(id="inst_1", name="Global Innovation Center", code="GIC01", category="MARKET")
            db.add(inst)
        
        if not db.query(models.OrgUnit).filter_by(id="dept_1").first():
            # 2. OrgUnit
            dept = models.OrgUnit(id="dept_1", institution_id="inst_1", name="Digital Transformation Team", unit_type="TEAM")
            db.add(dept)
            
        # ... (Similar checks for others or just rely on Primary Key constraints if we want simple)
        # For Demo, let's just make sure FinData is there
        
        # 3. User
        if not db.query(models.User).filter_by(id="user_1").first():
            user = models.User(
                id="user_1", 
                institution_id="inst_1", 
                org_unit_id="dept_1", 
                name="Alice Kim", 
                email="alice@gic.co.kr",
                current_salary=75000000.0
            )
            db.add(user)
        
        # ... Skipping hierarchy for brevity of edit, focus on missing FinData
        
        # 6. Productivity Data (Financial)
        if not db.query(models.FinancialPerformance).filter_by(institution_id="inst_1", year=2024).first():
            fin = models.FinancialPerformance(
                institution_id="inst_1",
                year=2024,
                revenue=12000000000.0, # 12B
                operating_expenses=4000000000.0, # 4B
                personnel_costs=5000000000.0, # 5B
                net_income=3000000000.0 # 3B
            )
            db.add(fin)
        
        if not db.query(models.HeadcountPlan).filter_by(institution_id="inst_1", year=2024).first():
            hc = models.HeadcountPlan(
                institution_id="inst_1",
                year=2024,
                authorized_count=50,
                current_count=48,
                required_count=52
            )
            db.add(hc)

        db.commit()
        print("Seeding Complete successfully!")
        
    except Exception as e:
        print(f"Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
