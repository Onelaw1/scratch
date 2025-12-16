from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
import uuid

from .. import models, schemas
from ..database import get_db
# RBAC dependencies
from ..dependencies import require_roles, require_permission

router = APIRouter(
    prefix="/productivity",
    tags=["Productivity Analysis"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(require_roles('ADMIN', 'HR_MANAGER'))]
)

@router.post("/financial-performance", response_model=schemas.FinancialPerformance)
def create_financial_performance(
    performance: schemas.FinancialPerformanceCreate,
    db: Session = Depends(get_db)
):
    # Check if entry exists for institution and year
    existing = db.query(models.FinancialPerformance).filter(
        models.FinancialPerformance.institution_id == performance.institution_id,
        models.FinancialPerformance.year == performance.year
    ).first()
    
    if existing:
        # Update existing
        existing.revenue = performance.revenue
        existing.operating_expenses = performance.operating_expenses
        existing.personnel_costs = performance.personnel_costs
        existing.net_income = performance.revenue - (performance.operating_expenses + performance.personnel_costs)
        db.commit()
        db.refresh(existing)
        return existing
    
    # Create new
    net_income = performance.revenue - (performance.operating_expenses + performance.personnel_costs)
    new_performance = models.FinancialPerformance(
        **performance.dict(),
        net_income=net_income
    )
    db.add(new_performance)
    db.commit()
    db.refresh(new_performance)
    return new_performance

@router.get("/financial-performance/{institution_id}", response_model=List[schemas.FinancialPerformance])
def get_financial_performance(
    institution_id: str,
    db: Session = Depends(get_db)
):
    return db.query(models.FinancialPerformance).filter(
        models.FinancialPerformance.institution_id == institution_id
    ).order_by(models.FinancialPerformance.year).all()

@router.get("/metrics/{institution_id}")
def get_productivity_metrics(
    institution_id: str,
    year: int = None,
    db: Session = Depends(get_db)
):
    # 1. Get Financial Data
    query = db.query(models.FinancialPerformance).filter(models.FinancialPerformance.institution_id == institution_id)
    if year:
        query = query.filter(models.FinancialPerformance.year == year)
    
    financials = query.order_by(models.FinancialPerformance.year).all()
    
    if not financials:
        return []

    # 2. Calculate FTE for the institution (Total)
    # [Strategic Context]
    # FTE(Full-Time Equivalent) 산정 방식:
    # 단순 정원(Headcount)이 아닌, 실제 투입된 "총 업무 시간 / 표준 근무 시간(2080시간)"으로 산출해야 정확한 생산성 분석이 가능함.
    # 현재 단계(MVP)에서는 별도의 FTE 이력 테이블이 없으므로, HeadcountPlan의 '현원(Current Count)'을 FTE 근사치로 활용함.
    # 추후 'WorkloadEntry'의 정밀 데이터를 기반으로 한 Bottom-up 방식의 FTE 산출 로직으로 고도화 필요.
    
    metrics = []
    
    for fin in financials:
        # Try to find HeadcountPlan for this year
        hc_plan = db.query(models.HeadcountPlan).filter(
            models.HeadcountPlan.institution_id == institution_id,
            models.HeadcountPlan.year == fin.year
        ).first()
        
        fte = 0.0
        if hc_plan and hc_plan.current_count:
            fte = float(hc_plan.current_count)
        else:
             # Fallback: 데이터가 없는 경우 0으로 처리 (Safety Net)
             fte = 0.0
        
        hcroi = 0.0
        hcva = 0.0
        
        # [Strategic Context] HCROI (Human Capital ROI)
        # 공식: (매출액 - (운영비용 - 인건비)) / 인건비
        # 의미: 인건비 1원 투입 시 창출되는 재무적 가치.
        # 해석: 이 수치가 1.0보다 커야 인건비 대비 이익이 발생하고 있음을 의미함.
        if fin.personnel_costs > 0:
            hcroi = (fin.revenue - fin.operating_expenses) / fin.personnel_costs
            
        # [Strategic Context] HCVA (Human Capital Value Added)
        # 공식: (매출액 - (운영비용 - 인건비)) / FTE
        # 의미: 직원 1인당(FTE 기준) 창출하는 부가가치 절대액.
        # 해석: 기업 규모와 관계없이 "개개인의 생산성"을 절대 비교할 수 있는 핵심 지표.
        if fte > 0:
            hcva = (fin.revenue - fin.operating_expenses) / fte
            
        metrics.append({
            "year": fin.year,
            "revenue": fin.revenue,
            "operating_expenses": fin.operating_expenses,
            "personnel_costs": fin.personnel_costs,
            "net_income": fin.net_income,
            "fte": fte,
            "hcroi": round(hcroi, 2),
            "hcva": round(hcva, 2)
        })
        
    return metrics
