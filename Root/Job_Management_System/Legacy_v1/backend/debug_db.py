
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.getcwd())

from backend.database import Base, SQLALCHEMY_DATABASE_URL
from backend import models

# Access the same DB as demo_seeder
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    db_path = os.path.join(os.getcwd(), "sql_app.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def debug_data():
    db = SessionLocal()
    try:
        print(f"Checking database at {SQLALCHEMY_DATABASE_URL}")
        
        fins = db.query(models.FinancialPerformance).all()
        print(f"Found {len(fins)} FinancialPerformance records")
        for f in fins:
            print(f" - ID: {f.id}, InstID: {f.institution_id}, Year: {f.year}")
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_data()
