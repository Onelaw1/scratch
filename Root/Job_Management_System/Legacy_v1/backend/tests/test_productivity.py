
import pytest
from backend.models import FinancialPerformance, Institution, HeadcountPlan

def setup_productivity_data(db):
    # Setup Data
    inst = Institution(id="inst-1", name="Test Institute", code="TEST01", category="MARKET")
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

def test_get_productivity_metrics(client, db_session):
    setup_productivity_data(db_session)
    
    response = client.get("/productivity/metrics/inst-1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    metric = data[0]
    
    assert metric["year"] == 2024
    assert metric["revenue"] == 1000.0
    assert metric["hcroi"] == 2.67 # Rounded
    assert metric["hcva"] == 80.0
