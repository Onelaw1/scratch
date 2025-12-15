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
    
    # In a real app, we would map by code. Here we just return the raw ERP data
    # combined with some system lookups to show the "Diff".
    
    diff_report = []
    for row in erp_data:
        # Try to find corresponding OrgUnit by name similarity or code (if we had it)
        # For MVP, we will assume we update by 'Name' if it exists, or show 'New'
        
        system_unit = db.query(models.OrgUnit).filter(models.OrgUnit.name.contains(row['dept_name'].split(" ")[0])).first()
        
        diff_report.append({
            "dept_code": row['dept_code'],
            "dept_name": row['dept_name'],
            "erp_budget": row['budget_millions'],
            "erp_to": row['authorized_to'],
            "system_budget": system_unit.budget if system_unit else 0,
            "system_to": system_unit.authorized_headcount if system_unit else 0,
            "status": "MATCH" if system_unit and system_unit.authorized_headcount == row['authorized_to'] else "DIFF",
            "system_id": system_unit.id if system_unit else None
        })
        
    return diff_report

@router.post("/sync")
def execute_erp_sync(db: Session = Depends(get_db)):
    """
    Executes the synchronization. Updates local OrgUnits with ERP data.
    """
    erp_data = erp_service.fetch_org_structure_data()
    updated_count = 0
    logs = []

    for row in erp_data:
        # Match by loose name matching for MVP
        system_unit = db.query(models.OrgUnit).filter(models.OrgUnit.name.contains(row['dept_name'].split(" ")[0])).first()
        
        if system_unit:
            system_unit.budget = row['budget_millions']
            system_unit.authorized_headcount = row['authorized_to']
            updated_count += 1
            logs.append(f"Updated {system_unit.name}: Budget={row['budget_millions']}, TO={row['authorized_to']}")
    
    # Create Log Entry
    # Mock Institution ID
    inst = db.query(models.Institution).first()
    
    sync_log = models.ERPSyncLog(
        status="SUCCESS",
        records_updated=updated_count,
        details=json.dumps(logs),
        institution_id=inst.id if inst else "unknown"
    )
    db.add(sync_log)
    db.commit()
    
    return {"status": "success", "updated": updated_count, "log_id": sync_log.id}

@router.get("/logs")
def get_sync_logs(db: Session = Depends(get_db)):
    return db.query(models.ERPSyncLog).order_by(models.ERPSyncLog.sync_date.desc()).all()
