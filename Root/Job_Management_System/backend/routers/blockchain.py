from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..database import get_db
from ..models import User
from ..services.blockchain_service import BlockchainService

router = APIRouter(
    prefix="/blockchain",
    tags=["Blockchain Certificate"],
    responses={404: {"description": "Not found"}},
)

service = BlockchainService()

@router.post("/issue/{user_id}")
def issue_certificate(user_id: str, db: Session = Depends(get_db)):
    """
    Issues a verified Blockchain Certificate for the user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return service.issue_certificate(user)
