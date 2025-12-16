from sqlalchemy import create_engine, text
import os

# Assuming database is at ./job_management.db based on previous context
DB_URL = "sqlite:///./job_management.db"

def migrate():
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        try:
            # Add columns one by one. SQLite doesn't support multiple ADD COLUMN in one statement standardly.
            # We ignore errors if column exists.
            columns = [
                "skills TEXT",
                "values TEXT",
                "attitudes TEXT",
                "knowledge TEXT",
                "previous_experience TEXT",
                "required_training TEXT"
            ]
            
            for col in columns:
                try:
                    conn.execute(text(f"ALTER TABLE job_descriptions ADD COLUMN {col}"))
                    print(f"Added column: {col}")
                except Exception as e:
                    print(f"Skipping {col}: {e}")
            
            print("Migration completed.")
        except Exception as e:
            print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
