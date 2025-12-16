from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.services.ml_service import TurnoverPredictor, CareerPathRecommender
# RBAC dependencies
from backend.dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/scientific/prediction",
    tags=["Predictive HR"],
    dependencies=[Depends(require_roles('ADMIN', 'HR_MANAGER'))]
)

# Global Instances (Simple In-Memory persistence for demo)
predictor = TurnoverPredictor()
recommender = CareerPathRecommender()

@router.post("/turnover/train")
def train_turnover_model(db: Session = Depends(get_db)):
    result = predictor.train_model(db)
    return result

@router.get("/turnover/{user_id}")
def get_turnover_risk(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Auto-train if needed
    if not predictor.is_trained:
        predictor.train_model(db)
        
    return predictor.predict_risk(user, db)

@router.get("/career/{user_id}")
def get_career_recommendations(user_id: str, db: Session = Depends(get_db)):
    return recommender.recommend_paths(user_id, db)
