import sys
import os
from sqlalchemy import create_engine, text

# Job Management System 루트 경로 추가
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

from backend.database import SQLALCHEMY_DATABASE_URL as DATABASE_URL

def fix_schema():
    """
    기존 테이블에 누락된 컬럼을 추가합니다.
    SQLAlchemy의 create_all은 기존 테이블을 갱신하지 않으므로, 
    ALTER TABLE을 사용하여 수동으로 컬럼을 추가해야 합니다.
    """
    print(f"데이터베이스 연결 중: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("컬럼 추가 작업 시작...")
        
        # 1. Job Series: ncs_code, ncs_name 추가
        try:
            conn.execute(text("ALTER TABLE job_series ADD COLUMN ncs_code VARCHAR"))
            print("[SUCCESS] job_series 테이블에 'ncs_code' 컬럼 추가됨.")
        except Exception as e:
            print(f"[INFO] job_series 'ncs_code' 추가 건너뜀 (이미 존재하거나 오류): {e}")

        try:
            conn.execute(text("ALTER TABLE job_series ADD COLUMN ncs_name VARCHAR"))
            print("[SUCCESS] job_series 테이블에 'ncs_name' 컬럼 추가됨.")
        except Exception as e:
            print(f"[INFO] job_series 'ncs_name' 추가 건너뜀 (이미 존재하거나 오류): {e}")

        # 2. Job Position: grade, is_future_model 추가
        try:
            conn.execute(text("ALTER TABLE job_positions ADD COLUMN grade VARCHAR"))
            print("[SUCCESS] job_positions 테이블에 'grade' 컬럼 추가됨.")
        except Exception as e:
            print(f"[INFO] job_positions 'grade' 추가 건너뜀: {e}")

        try:
            conn.execute(text("ALTER TABLE job_positions ADD COLUMN is_future_model BOOLEAN DEFAULT 0"))
            print("[SUCCESS] job_positions 테이블에 'is_future_model' 컬럼 추가됨.")
        except Exception as e:
            print(f"[INFO] job_positions 'is_future_model' 추가 건너뜀: {e}")

        # 3. Job Task: action_verb, task_object, AI columns 추가
        columns_to_add = [
            ("job_tasks", "action_verb", "VARCHAR"),
            ("job_tasks", "task_object", "VARCHAR"),
            ("job_tasks", "ai_substitution", "FLOAT DEFAULT 0.0"),
            ("job_tasks", "ai_augmentation", "FLOAT DEFAULT 0.0"),
            ("job_tasks", "ai_generation", "FLOAT DEFAULT 0.0"),
        ]
        
        for table, col, dtype in columns_to_add:
            try:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {dtype}"))
                print(f"[SUCCESS] {table} 테이블에 '{col}' 컬럼 추가됨.")
            except Exception as e:
                print(f"[INFO] {table} '{col}' 추가 건너뜀: {e}")

        conn.commit()
        print("스키마 수동 업데이트 완료.")

if __name__ == "__main__":
    fix_schema()
