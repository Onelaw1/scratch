import sys
import os
from sqlalchemy import create_engine

# Add Job Management System root to path
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

from backend.models import Base, StrategicAnalysis
from backend.database import SQLALCHEMY_DATABASE_URL as DATABASE_URL

def update_schema():
    print(f"Connecting to database: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    
    print("Creating 'strategic_analyses' table...")
    # Create only the new table
    StrategicAnalysis.__table__.create(bind=engine, checkfirst=True)
    
    print("Schema update complete.")

if __name__ == "__main__":
    update_schema()
