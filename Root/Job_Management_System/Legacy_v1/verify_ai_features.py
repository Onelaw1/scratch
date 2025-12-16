
import sys
import os
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add Root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from backend.main import app
from backend.database import Base, get_db
from backend import models

# In-Memory DB
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
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

def setup_data():
    db = TestingSessionLocal()
    
    # User for Prediction
    hire_date = date.today() - timedelta(days=365*4) # 4 Years (Stagnation risk)
    user = models.User(
        id="user_pred", 
        name="Predict User", 
        hire_date=hire_date,
        current_salary=40000000 # Low Salary
    )
    db.add(user)
    
    # Pulse Data (Negative)
    for i in range(3):
        pulse = models.PulseCheck(
            id=f"pulse_{i}",
            user_id="user_pred",
            date=date.today() - timedelta(days=i),
            mood_score=2 # Low Mood
        )
        db.add(pulse)
        
    # Job Position for JD Validation
    pos = models.JobPosition(id="pos_jd", title="AI Engineer", series_id="ser_1", grade="G3")
    db.add(pos)
    
    db.commit()
    db.close()

def verify_save_jd():
    print("\n--- Verifying Save JD ---")
    payload = {
        "position_id": "pos_jd",
        "overview": "This is a saved overview.",
        "responsibilities": "- Task A\n- Task B",
        "qualifications": "- Good Python Skills"
    }
    
    res = client.post("/ai/save-jd", json=payload)
    if res.status_code == 200:
        print("[PASS] JD Save Endpoint")
        
        # Verify DB content
        db = TestingSessionLocal()
        jd = db.query(models.JobDescription).filter(models.JobDescription.job_position_id == "pos_jd").first()
        if jd and jd.summary == "This is a saved overview.":
            print("[PASS] Validation: Data Persisted Correctly")
        else:
            print(f"[FAIL] Data Verification Failed: {jd.summary if jd else 'No JD'}")
        db.close()
    else:
        print(f"[FAIL] Save Endpoint Failed: {res.text}")

def verify_turnover_prediction():
    print("\n--- Verifying Turnover Prediction ---")
    res = client.get("/scientific/prediction/turnover/user_pred")
    
    if res.status_code == 200:
        data = res.json()
        print(f"Risk Score: {data['risk_score']} ({data['risk_level']})")
        factors = data['factors']
        print(f"Factors: {factors}")
        
        # Expect High Risk
        # 1. Salary Ratio 40/60 = 0.66 (<0.85 -> +0.3)
        # 2. Tenure 4yr (>3 -> +0.15)
        # 3. Pulse Mood 2 (<3 -> +0.25)
        # Base 0.2 + 0.3 + 0.15 + 0.25 = 0.9
        
        if data['risk_score'] >= 0.8:
            print("[PASS] Risk Calculation Logic Validated (High Risk detected)")
        else:
            print(f"[FAIL] Risk Score too low: {data['risk_score']}")
            
        if 'pulse_risk' in factors and 'tenure_risk' in factors:
             print("[PASS] New Factors (Pulse, Tenure) correctly identified")
        else:
             print("[FAIL] Missing Factors")
    else:
        print(f"[FAIL] Prediction Endpoint Failed: {res.text}")

if __name__ == "__main__":
    setup_data()
    verify_save_jd()
    verify_turnover_prediction()
