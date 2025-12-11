import sqlite3
import os

def update_schema():
    db_path = "sql_app.db"
    if not os.path.exists(db_path):
        print("Database not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add standard_time
        cursor.execute("ALTER TABLE workload_entries ADD COLUMN standard_time FLOAT DEFAULT 0.0")
        print("Added standard_time column.")
    except sqlite3.OperationalError:
        print("standard_time column already exists.")

    try:
        # Add volume
        cursor.execute("ALTER TABLE workload_entries ADD COLUMN volume FLOAT DEFAULT 0.0")
        print("Added volume column.")
    except sqlite3.OperationalError:
        print("volume column already exists.")

    try:
        # Add fte_value
        cursor.execute("ALTER TABLE workload_entries ADD COLUMN fte_value FLOAT DEFAULT 0.0")
        print("Added fte_value column.")
    except sqlite3.OperationalError:
        print("fte_value column already exists.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_schema()
