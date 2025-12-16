import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

# Job Management System 루트 경로 추가
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_path)

from backend.main import app
from backend.database import Base, get_db
from backend import models

# 테스트용 DB 설정 (메모리 DB 사용 가능하지만, 여기서는 개발 DB에 직접 테스트 데이터를 넣고 확인 후 롤백하거나 유지함)
# 여기서는 개발 DB를 그대로 사용하되, 테스트 데이터를 주입합니다.
from backend.database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def verify_job_classification():
    """
    직무 분류 체계 API (계층형, 매트릭스형)를 검증합니다.
    """
    print("=== 직무 분류 체계 검증 시작 ===")
    
    db = TestingSessionLocal()
    
    # 1. 테스트 데이터 생성
    print("1. 테스트 데이터 생성 중...")
    
    # Job Group
    group = models.JobGroup(id="TEST_GROUP_01", name="경영지원그룹")
    db.merge(group) # merge를 사용하여 중복 시 업데이트
    
    # Job Series
    series = models.JobSeries(id="TEST_SERIES_01", group_id="TEST_GROUP_01", name="인사운영직", ncs_code="02020201")
    db.merge(series)
    
    # Job Position
    position = models.JobPosition(id="TEST_POS_01", series_id="TEST_SERIES_01", title="채용담당자", grade="G4")
    db.merge(position)
    
    # Job Task
    task = models.JobTask(id="TEST_TASK_01", job_position_id="TEST_POS_01", task_name="채용 공고 게시", action_verb="게시하다", task_object="채용 공고")
    db.merge(task)
    
    # Work Item
    work_item = models.WorkItem(id="TEST_ITEM_01", job_task_id="TEST_TASK_01", name="채용 사이트 업로드", frequency="WEEKLY")
    db.merge(work_item)
    
    db.commit()
    print("테스트 데이터 생성 완료.")
    
    # 2. 계층형 조회 (Tree View) 검증
    print("\n2. 계층형 조회 (Tree View) API 호출...")
    response = client.get("/classification/hierarchy")
    
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] 응답 코드 200 OK")
        # 간단한 구조 확인
        found = False
        for g in data:
            if g['id'] == "TEST_GROUP_01":
                found = True
                print(f"  - 그룹 확인: {g['name']}")
                if g['children'] and g['children'][0]['id'] == "TEST_SERIES_01":
                    print(f"  - 직렬 확인: {g['children'][0]['name']}")
        
        if not found:
            print("[WARNING] 테스트 그룹을 찾을 수 없습니다.")
    else:
        print(f"[FAIL] 응답 코드: {response.status_code}")
        print(response.text)

    # 3. 매트릭스형 조회 (Matrix View) 검증
    print("\n3. 매트릭스형 조회 (Matrix View) API 호출...")
    response = client.get("/classification/matrix")
    
    if response.status_code == 200:
        data = response.json()
        print(f"[SUCCESS] 응답 코드 200 OK")
        # 데이터 확인
        found = False
        for row in data:
            if row['group_name'] == "경영지원그룹" and row['work_item_name'] == "채용 사이트 업로드":
                found = True
                print(f"  - 매트릭스 행 확인: {row}")
                break
        
        if not found:
            print("[WARNING] 테스트 매트릭스 데이터를 찾을 수 없습니다.")
    else:
        print(f"[FAIL] 응답 코드: {response.status_code}")
        print(response.text)

    db.close()
    print("\n=== 검증 완료 ===")

if __name__ == "__main__":
    verify_job_classification()
