from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from .. import crud, models, schemas
from ..database import get_db
from ..services.erp_mock import ERPMockService
import json

router = APIRouter(
    prefix="/erp",
    tags=["Enterprise Integration"],
    responses={404: {"description": "Not found"}},
)

erp_service = ERPMockService()

@router.get("/preview", response_model=List[Dict[str, Any]])
def preview_erp_sync(db: Session = Depends(get_db)):
    """
    Returns a unified view of System Data vs ERP Data differences.
    """
    erp_data = erp_service.fetch_org_structure_data()
    
    diff_report = []
    for row in erp_data:
        # 1. Try to find by Exact Code first (if we had it), then Name
        # Using name.contains is risky, but okay for MVP demo
        search_term = row['dept_name'].split(" ")[0]
        system_unit = db.query(models.OrgUnit).filter(models.OrgUnit.name.contains(search_term)).first()
        
        status = "MATCH"
        sys_budget = 0
        sys_to = 0
        sys_id = None
        
        if not system_unit:
            status = "MISSING_IN_SYSTEM"
        else:
            sys_id = system_unit.id
            sys_budget = system_unit.budget
            sys_to = system_unit.authorized_headcount
            
            if sys_budget != row['budget_millions'] or sys_to != row['authorized_to']:
                status = "DIFF"

        diff_report.append({
            "dept_code": row['dept_code'],
            "dept_name": row['dept_name'],
            "erp_budget": row['budget_millions'],
            "erp_to": row['authorized_to'],
            "system_budget": sys_budget,
            "system_to": sys_to,
            "status": status,
            "system_id": sys_id
        })
        
    return diff_report

@router.post("/sync")
def execute_erp_sync(db: Session = Depends(get_db)):
    """
    Executes the synchronization. Updates local OrgUnits with ERP data.
    """
    erp_data = erp_service.fetch_org_structure_data()
    stats = {"updated": 0, "missing": 0, "unchanged": 0}
    logs = []

    for row in erp_data:
        search_term = row['dept_name'].split(" ")[0]
        system_unit = db.query(models.OrgUnit).filter(models.OrgUnit.name.contains(search_term)).first()
        
        if not system_unit:
            stats["missing"] += 1
            logs.append(f"SKIP: Could not find system unit for ERP Dept '{row['dept_name']}'")
            continue
            
        # Check if update needed
        if system_unit.budget != row['budget_millions'] or system_unit.authorized_headcount != row['authorized_to']:
            old_budget = system_unit.budget
            old_to = system_unit.authorized_headcount
            
            system_unit.budget = row['budget_millions']
            system_unit.authorized_headcount = row['authorized_to']
            
            stats["updated"] += 1
            logs.append(f"UPDATE {system_unit.name}: Budget {old_budget}->{row['budget_millions']}, TO {old_to}->{row['authorized_to']}")
        else:
            stats["unchanged"] += 1
    
    # Create Log Entry
    inst = db.query(models.Institution).first()
    
    sync_log = models.ERPSyncLog(
        status="SUCCESS" if stats["missing"] == 0 else "PARTIAL_SUCCESS",
        records_updated=stats["updated"],
        details=json.dumps(logs),
        institution_id=inst.id if inst else "unknown"
    )
    db.add(sync_log)
    db.commit()
    
    return {
        "status": "success", 
        "updated": stats["updated"], 
        "missing": stats["missing"],
        "unchanged": stats["unchanged"],
        "log_id": sync_log.id
    }

@router.get("/logs")
def get_sync_logs(db: Session = Depends(get_db)):
    return db.query(models.ERPSyncLog).order_by(models.ERPSyncLog.sync_date.desc()).all()
