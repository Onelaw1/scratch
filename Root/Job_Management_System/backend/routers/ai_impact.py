from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from .. import models, schemas, database

router = APIRouter(
    prefix="/ai-impact",
    tags=["ai-impact"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/simulate-fte/{position_id}")
def simulate_ai_adjusted_fte(
    position_id: str, 
    adoption_rate: float = 1.0, 
    efficiency_factor: float = 0.3,
    db: Session = Depends(get_db)
):
    """
    Calculates the AI-Adjusted Dynamic FTE (AI-ADFM) for a given Job Position.
    
    Formula:
    FTE_ai = Sum( (Volume * ST * (1 - Impact)) / AnnualHours ) + FTE_new
    
    Where Impact = (Substitution * 1.0) + (Augmentation * EfficiencyFactor)
    """
    
    # 1. Fetch Position and Tasks
    position = db.query(models.JobPosition).filter(models.JobPosition.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Job Position not found")
        
    tasks = position.tasks
    
    # 2. Calculate FTE
    annual_hours = 1920.0
    total_fte_old = 0.0
    total_fte_ai = 0.0
    
    breakdown = []
    
    for task in tasks:
        # Aggregate workload entries for this task to get total Volume * ST
        # In a real scenario, we might average ST or sum Volume across users.
        # For simplicity, let's assume one entry per task or sum them up.
        entries = db.query(models.WorkloadEntry).filter(models.WorkloadEntry.task_id == task.id).all()
        
        task_volume = sum(e.volume for e in entries)
        task_st = entries[0].standard_time if entries else 0.0 # Assume consistent ST for the task
        
        raw_hours = task_volume * task_st
        fte_old = raw_hours / annual_hours
        
        # AI Impact Calculation
        # Impact = (Sub * 1.0) + (Aug * Eff_Factor)
        # We scale by Adoption Rate (alpha)
        impact_score = (task.ai_substitution * 1.0) + (task.ai_augmentation * efficiency_factor)
        impact_score *= adoption_rate
        
        # Cap impact at 1.0 (cannot save more than 100% time)
        impact_score = min(impact_score, 1.0)
        
        # Adjusted Hours
        adjusted_hours = raw_hours * (1 - impact_score)
        
        # Add Generation (New Tasks) - stored as FTE directly or Hours? 
        # Model says 'ai_generation' is float. Let's assume it's "Additional FTE required" per unit of volume? 
        # Or just a static FTE add-on?
        # Let's assume ai_generation is a coefficient of increased complexity/verification needed, 
        # effectively negative impact, or just add it.
        # White paper says: + FTE_new_tasks.
        # Let's treat ai_generation as a % increase in workload for verification.
        # Adjusted = Raw * (1 - Impact + Generation)
        
        generation_factor = task.ai_generation * adoption_rate
        final_hours = raw_hours * (1 - impact_score + generation_factor)
        
        fte_ai = final_hours / annual_hours
        
        total_fte_old += fte_old
        total_fte_ai += fte_ai
        
        breakdown.append({
            "task_name": task.task_name,
            "fte_old": round(fte_old, 4),
            "fte_ai": round(fte_ai, 4),
            "impact_score": round(impact_score, 2),
            "generation_factor": round(generation_factor, 2),
            "efficiency_gain_percent": round((1 - (fte_ai/fte_old if fte_old > 0 else 1)) * 100, 1)
        })
        
    return {
        "position_name": position.name,
        "total_fte_old": round(total_fte_old, 4),
        "total_fte_ai": round(total_fte_ai, 4),
        "net_change_percent": round(((total_fte_ai - total_fte_old) / total_fte_old * 100) if total_fte_old > 0 else 0, 1),
        "breakdown": breakdown
    }
