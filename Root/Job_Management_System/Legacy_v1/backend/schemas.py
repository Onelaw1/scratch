from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import date, datetime
from enum import Enum

# Enums
class JobGrade(str, Enum):
    G1 = "G1"
    G2 = "G2"
    G3 = "G3"
    G4 = "G4"
    G5 = "G5"
    EXECUTIVE = "EXECUTIVE"

class AISource(str, Enum):
    USER_INPUT = "USER_INPUT"
    AI_GENERATED = "AI_GENERATED"
    AI_REFINED = "AI_REFINED"

class ComplianceStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    VIOLATION = "VIOLATION"

# --- Job Components ---
class JobTaskBase(BaseModel):
    name: str
    importance: int = 3
    frequency: str = "Daily"
    is_essential: bool = True

class JobTaskCreate(JobTaskBase):
    pass

class JobTask(JobTaskBase):
    id: str
    job_id: str
    class Config:
        from_attributes = True

class JobRequirementBase(BaseModel):
    category: str
    content: str
    is_blind_violation: bool = False

class JobRequirementCreate(JobRequirementBase):
    pass

class JobRequirement(JobRequirementBase):
    id: str
    job_id: str
    class Config:
        from_attributes = True

# --- AI & Audit Logs ---
class FairnessAuditLogBase(BaseModel):
    check_type: str
    status: ComplianceStatus
    message: Optional[str] = None

class FairnessAuditLog(FairnessAuditLogBase):
    id: str
    detected_at: datetime
    class Config:
        from_attributes = True

# --- Job Position ---
class JobPositionBase(BaseModel):
    title: str
    summary: Optional[str] = None
    strategic_goal_link: Optional[str] = None
    ncs_code_id: Optional[str] = None

class JobPositionCreate(JobPositionBase):
    pass

class JobPosition(JobPositionBase):
    id: str
    creation_source: AISource
    ai_confidence_score: float
    grade_prediction: Optional[JobGrade] = None
    
    tasks: List[JobTask] = []
    requirements: List[JobRequirement] = []
    audit_logs: List[FairnessAuditLog] = []
    
    class Config:
        from_attributes = True

# --- Job Evaluation Schemas ---
class JobEvaluationCriteriaBase(BaseModel):
    category: str
    name: str
    weight: float = 1.0
    description: Optional[str] = None

class JobEvaluationCriteria(JobEvaluationCriteriaBase):
    id: str
    class Config:
        from_attributes = True

class JobEvaluationScoreBase(BaseModel):
    criteria_id: str
    score: float
    notes: Optional[str] = None

class JobEvaluationScore(JobEvaluationScoreBase):
    id: str
    class Config:
        from_attributes = True

class JobEvaluationBase(BaseModel):
    total_score: float = 0.0
    final_grade: Optional[JobGrade] = None
    ai_suggested_grade: Optional[JobGrade] = None
    evaluator_comment: Optional[str] = None

class JobEvaluationCreate(JobEvaluationBase):
    scores: List[JobEvaluationScoreBase]

class JobEvaluation(JobEvaluationBase):
    id: str
    job_id: str
    scores: List[JobEvaluationScore] = []
    class Config:
        from_attributes = True
