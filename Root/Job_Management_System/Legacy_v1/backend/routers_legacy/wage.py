from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from pydantic import BaseModel
from ..database import get_db
from ..services.wage_simulation import WageSimulationService

router = APIRouter(
    prefix="/wage",
    tags=["Wage Simulation"],
    responses={404: {"description": "Not found"}},
)

service = WageSimulationService()

class SimulationRequest(BaseModel):
    spread: float = 0.3    # Band Spread (e.g. 0.3 = 30%)
    base_increase: float = 0.02 # Base Increase (e.g. 0.02 = 2%)

@router.post("/simulate")
def run_wage_simulation(req: SimulationRequest, db: Session = Depends(get_db)):
    """
    Runs the "Seniority -> Job-Based" Wage Transition Simulation.
    """
    result = service.run_simulation(db, req.spread, req.base_increase)
    return result
