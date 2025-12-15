import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database import get_db, Base
from backend.models import FinancialPerformance, Institution, HeadcountPlan

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Setup Data
    inst = Institution(id="inst-1", name="Test Institute", code="TEST01")
    db.add(inst)
    
    # Financial Data
    # Revenue: 1000, OpEx: 200, Personnel: 300
    # Net Income: 1000 - 200 - 300 = 500
    # HCROI: (1000 - 200) / 300 = 800 / 300 = 2.66...
    fin = FinancialPerformance(
        id="fin-1", institution_id="inst-1", year=2024,
        revenue=1000.0, operating_expenses=200.0, personnel_costs=300.0, net_income=500.0
    )
    db.add(fin)
    
    # Headcount Data (FTE)
    # Current Count: 10
    # HCVA: (1000 - 200) / 10 = 800 / 10 = 80
    hc = HeadcountPlan(
        id="hc-1", institution_id="inst-1", year=2024,
        authorized_count=10, current_count=10, required_count=10
    )
    db.add(hc)
    
    db.commit()
    yield db
    db.close()

def test_get_productivity_metrics(test_db):
    response = client.get("/productivity/metrics/inst-1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    metric = data[0]
    
    assert metric["year"] == 2024
    assert metric["revenue"] == 1000.0
    assert metric["hcroi"] == 2.67 # Rounded
    assert metric["hcva"] == 80.0
