from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from .. import crud, models, schemas
from ..database import get_db
import uuid
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/workforce",
    tags=["workforce"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN', 'HR_MANAGER'))]
)

@router.get("/gap-analysis")
def get_gap_analysis(db: Session = Depends(get_db)):
    """
    [Strategic Context] Workforce Gap Analysis (인력 수급 분석)
    
    1. Authorized (정원): 경영진 및 예산 부서에서 승인한 TO(Table of Organization). 기획 예산 관점.
    2. Required (적정인력): 직무 조사(Workload Analysis)를 통해 산출된 과학적 필요 인력(FTE). 현장 업무 관점.
    
    Gap = Authorized - Required
    - Positive Gap (+) : 정원 > 적정인력 (Overstaffed). 잉여 인력이 존재하므로 직무 재배치(Redeployment) 또는 효율화 필요.
    - Negative Gap (-) : 정원 < 적정인력 (Understaffed). 업무 과부하 상태이므로 신규 채용(Hiring) 또는 업무 감축(Process Innovation) 필요.
    
    This API provides the data to resolve the conflict between "Budgeted View" and "Operational View".
    """
    
    # 1. Get all Org Units
    org_units = db.query(models.OrgUnit).all()
    
    result = []
    
    for unit in org_units:
        # 2. Get Current Headcount (PO)
        current_count = db.query(models.User).filter(models.User.org_unit_id == unit.id).count()
        
        # 3. Get Authorized Headcount (TO) - Assume current year (e.g., 2025)
        # For MVP, defaulting to 2025. In prod, pass year as param.
        headcount_plan = db.query(models.HeadcountPlan).filter(
            models.HeadcountPlan.org_unit_id == unit.id,
            models.HeadcountPlan.year == 2025
        ).first()
        
        authorized_count = headcount_plan.authorized_count if headcount_plan else 0.0
        
        # 4. Get Required Headcount (FTE total)
        # This requires summing up FTE of all users in this unit
        # FTE comes from WorkloadEntry -> User -> OrgUnit
        # Optimized query: Join WorkloadEntry, User, filter by Unit
        
        total_fte = db.query(func.sum(models.WorkloadEntry.fte))\
            .join(models.User)\
            .filter(models.User.org_unit_id == unit.id)\
            .scalar() or 0.0
            
        unit_data = {
            "id": unit.id,
            "unit_name": unit.name,
            "unit_type": unit.unit_type,
            "current_count": current_count,
            "authorized_count": authorized_count,
            "required_count": round(total_fte, 2),
            "gap": round(authorized_count - total_fte, 2)
        }
        result.append(unit_data)
        
    return result

@router.post("/headcount-plan")
def save_headcount_plan(plan: schemas.HeadcountPlanCreate, db: Session = Depends(get_db)):
    # Check if exists for year/unit
    existing = db.query(models.HeadcountPlan).filter(
        models.HeadcountPlan.org_unit_id == plan.org_unit_id,
        models.HeadcountPlan.year == plan.year
    ).first()
    
    if existing:
        existing.authorized_count = plan.authorized_count
        db.commit()
        db.refresh(existing)
        return existing
    
    new_plan = models.HeadcountPlan(
        id=str(uuid.uuid4()),
        institution_id=plan.institution_id,
        org_unit_id=plan.org_unit_id,
        year=plan.year,
        authorized_count=plan.authorized_count,
        # We could auto-calc current/required here, but usually those are dynamic
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan

@router.get("/dual-tenure", response_model=List[Dict[str, Any]])
def get_dual_tenure_analysis(
    org_unit_id: str = None,
    db: Session = Depends(get_db)
):
    """
    [Strategic Context]
    Dual Tenure System (이원화된 근속연수 관리):
    1. Absolute Tenure (절대 근속): 입사일부터 현재까지의 총 기간. 회사에 대한 Loyalty 및 조직 이해도를 대변함.
    2. Job Tenure (직무 근속): 현재 수행 중인 특정 직무(Job Position)의 수행 기간. 해당 직무에 대한 전문성(Expertise) 및 숙련도를 대변함.
    
    Why this matters?
    - 기존 인사관리는 '절대 근속'만 중시하여(연공서열), 직무 전문성이 낮은 고호봉자가 양산됨.
    - '직무 근속'을 별도로 관리함으로써, 순환보직의 폐해를 막고 전문가(Specialist) 양성 기반을 마련함.
    """
    from datetime import date
    
    query = db.query(models.User)
    if org_unit_id:
        query = query.filter(models.User.org_unit_id == org_unit_id)
        
    users = query.all()
    today = date.today()
    result = []
    
    for user in users:
        # 1. Absolute Tenure Calculation
        absolute_years = 0.0
        if user.hire_date:
            days = (today - user.hire_date).days
            absolute_years = round(days / 365.25, 1)
            
        # 2. Job Tenure Calculation
        # Find active position (most recent assignment)
        # We look for the User's JobPositions. Ideally need to filter by 'Active'.
        # Assuming the one with latest assignment_date is active.
        job_years = 0.0
        active_position = None
        
        if user.job_positions:
            # Sort by assignment date desc
            sorted_positions = sorted(
                [p for p in user.job_positions if p.assignment_date], 
                key=lambda x: x.assignment_date, 
                reverse=True
            )
            
            if sorted_positions:
                active_position = sorted_positions[0]
                days = (today - active_position.assignment_date).days
                job_years = round(days / 365.25, 1)
        
        result.append({
            "user_id": user.id,
            "name": user.name,
            "org_unit_name": user.org_unit.name if user.org_unit else "Unknown",
            "position_title": active_position.title if active_position else "N/A",
            "absolute_tenure": absolute_years,
            "job_tenure": job_years,
            # Gap Analysis: Job Tenure가 Absolute Tenure에 비해 현저히 낮으면 잦은 순환보직을 의미함.
            "specialization_ratio": round((job_years / absolute_years * 100), 1) if absolute_years > 0 else 0.0
        })
        
    return result
