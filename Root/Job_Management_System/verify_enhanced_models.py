from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models_enhanced import Base, Institution, User, JobPosition, JobSeries, JobGroup
from backend.database import SQLALCHEMY_DATABASE_URL

# Use SQLite for fast in-memory verification
TEST_DATABASE_URL = "sqlite:///:memory:"

def verify_models():
    print("Verifying Enhanced Models...")
    try:
        engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully.")
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Test Basic Insertion
        group = JobGroup(name="Management")
        db.add(group)
        db.commit()
        db.refresh(group)
        print(f"✅ JobGroup created: {group.name}")
        
        series = JobSeries(name="HR Manager", group_id=group.id, ncs_code="02020201")
        db.add(series)
        db.commit()
        print(f"✅ JobSeries created with NCS Code: {series.ncs_code}")
        
        print("All verification steps passed!")
        
    except Exception as e:
        print(f"❌ Verification Failed: {e}")
        raise e

if __name__ == "__main__":
    verify_models()
