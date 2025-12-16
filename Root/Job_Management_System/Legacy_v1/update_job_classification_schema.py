import sys
import os
from sqlalchemy import create_engine, inspect

# Job Management System 루트 경로 추가
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

from backend.models import Base, JobGroup, JobSeries, JobPosition, JobTask, WorkItem, TaskDependency, JobEvaluation, JobEvaluationScore, JobDescription
from backend.database import SQLALCHEMY_DATABASE_URL as DATABASE_URL

def update_schema():
    """
    직무 분류 체계(Job Classification) 관련 테이블을 생성합니다.
    기존 테이블이 있으면 건너뛰고, 없는 테이블만 생성합니다.
    """
    print(f"데이터베이스 연결 중: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)
    
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print(f"현재 존재하는 테이블: {existing_tables}")

    # 생성할 테이블 목록 정의
    target_tables = [
        "job_groups",
        "job_series",
        "job_positions",
        "job_tasks",
        "work_items",
        "task_dependencies",
        "job_evaluations",
        "job_evaluation_scores",
        "job_descriptions"
    ]

    print("테이블 생성 시작...")
    # checkfirst=True 옵션은 테이블이 존재하면 생성을 건너뜁니다.
    # 하지만 여기서는 명시적으로 로그를 남기기 위해 create_all을 사용하되, 
    # SQLAlchemy가 알아서 처리하도록 합니다.
    Base.metadata.create_all(bind=engine, checkfirst=True)
    
    # 생성 확인
    inspector = inspect(engine)
    current_tables = inspector.get_table_names()
    
    for table in target_tables:
        if table in current_tables:
            print(f"[OK] 테이블 '{table}' 확인됨.")
        else:
            print(f"[ERROR] 테이블 '{table}' 생성 실패!")

    print("스키마 업데이트 완료.")

if __name__ == "__main__":
    update_schema()
