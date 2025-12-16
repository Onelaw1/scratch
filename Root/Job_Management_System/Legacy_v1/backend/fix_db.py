from sqlalchemy import create_engine
from database import engine, Base
import models

def fix_db():
    print("Creating all tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_db()
