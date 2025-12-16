from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, Text, Enum, Date, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import uuid
import enum

def generate_uuid():
    return str(uuid.uuid4())

# --- Enums for Public Sector & AI ---
class JobGrade(str, enum.Enum):
    G1 = "G1"
    G2 = "G2"
    G3 = "G3"
    G4 = "G4"
    G5 = "G5"
    EXECUTIVE = "EXECUTIVE"

class AISource(str, enum.Enum):
    USER_INPUT = "USER_INPUT"
    AI_GENERATED = "AI_GENERATED"
    AI_REFINED = "AI_REFINED"

class ComplianceStatus(str, enum.Enum):
    PASS = "PASS"
    WARNING = "WARNING" # Bias suspected
    VIOLATION = "VIOLATION" # Legal issue

# =========================================================
# 1. NCS (National Competency Standards) Integration
#    - The Foundation of Public HR
# =========================================================

class NCSCode(Base):
    """
    Standard NCS Data. Read-only reference usually.
    """
    __tablename__ = "ncs_codes"
    id = Column(String, primary_key=True, default=generate_uuid)
    code = Column(String, unique=True, nullable=False) # e.g., 02010101
    name = Column(String, nullable=False) # e.g., 경영기획
    category = Column(String, nullable=True) # 대분류
    
    competencies = relationship("NCSCompetency", back_populates="ncs_code")

class NCSCompetency(Base):
    __tablename__ = "ncs_competencies"
    id = Column(String, primary_key=True, default=generate_uuid)
    ncs_id = Column(String, ForeignKey("ncs_codes.id"))
    
    unit_name = Column(String, nullable=False) # 능력단위명
    type = Column(String, nullable=False) # Knowledge(k), Skill(s), Attitude(a)
    description = Column(Text, nullable=True)
    
    ncs_code = relationship("NCSCode", back_populates="competencies")

# =========================================================
# 2. AI-Native Job Architecture
# =========================================================

class JobPosition(Base):
    """
    AI-Constructed Job Position.
    """
    __tablename__ = "job_positions"
    id = Column(String, primary_key=True, default=generate_uuid)
    
    # Core Identity
    title = Column(String, nullable=False)
    strategic_goal_link = Column(String, nullable=True) # ID or Text link to Strategy
    
    # NCS Alignment (Public Sector Requirement)
    ncs_code_id = Column(String, ForeignKey("ncs_codes.id"), nullable=True)
    
    # AI Metadata
    creation_source = Column(Enum(AISource), default=AISource.AI_GENERATED)
    ai_confidence_score = Column(Float, default=0.0) # How confident is AI in this design?
    
    # 3-Tier Job Structure
    summary = Column(Text, nullable=True)
    grade_prediction = Column(Enum(JobGrade), nullable=True) # AI Predicted Grade
    
    ncs_code = relationship("NCSCode")
    tasks = relationship("JobTask", back_populates="job", cascade="all, delete-orphan")
    requirements = relationship("JobRequirement", back_populates="job", cascade="all, delete-orphan")
    audit_logs = relationship("FairnessAuditLog", back_populates="target_job")

class JobTask(Base):
    __tablename__ = "job_tasks"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_id = Column(String, ForeignKey("job_positions.id"))
    
    name = Column(String, nullable=False)
    importance = Column(Integer, default=3)
    frequency = Column(String, default="Daily")
    
    # AI Logic
    is_essential = Column(Boolean, default=True) # Suggested by AI as essential
    
    job = relationship("JobPosition", back_populates="tasks")

class JobRequirement(Base):
    __tablename__ = "job_requirements"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_id = Column(String, ForeignKey("job_positions.id"))
    
    category = Column(String, nullable=False) # Knowledge, Skill, Attitude, Certification
    content = Column(String, nullable=False)
    
    # Blind Hiring Support
    is_blind_violation = Column(Boolean, default=False) # e.g. "Male only" -> Flagged
    
    job = relationship("JobPosition", back_populates="requirements")

# =========================================================
# 3. AI Intelligence & Audit Logs
# =========================================================

class AIGenerationLog(Base):
    """
    Tracks WHY and HOW the AI generated this content.
    Crucial for "Explainable HR" in public sector.
    """
    __tablename__ = "ai_generation_logs"
    id = Column(String, primary_key=True, default=generate_uuid)
    target_type = Column(String, nullable=False) # JOB, EVALUATION
    target_id = Column(String, nullable=False)
    
    prompt_context = Column(Text, nullable=True) # What triggered AI
    metrics_used = Column(JSON, nullable=True) # Key factors considered
    reasoning = Column(Text, nullable=True) # AI's explanation
    
    created_at = Column(DateTime, default=func.now())

class FairnessAuditLog(Base):
    """
    The "Fairness Engine" Output.
    """
    __tablename__ = "fairness_audit_logs"
    id = Column(String, primary_key=True, default=generate_uuid)
    target_job_id = Column(String, ForeignKey("job_positions.id"), nullable=True)
    
    check_type = Column(String, nullable=False) # GENDER_BIAS, AGE_BIAS, GRADE_INFLATION
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.PASS)
    score_deviation = Column(Float, default=0.0) # e.g. +1.5 above audit norm
    
    message = Column(Text, nullable=True) # "Warning: Requirement contains gendered language"
    detected_at = Column(DateTime, default=func.now())
    
    target_job = relationship("JobPosition", back_populates="audit_logs")

# =========================================================
# 4. Job Evaluation System (Restored & AI-Enhanced)
# =========================================================

class EvaluationSession(Base):
    __tablename__ = "evaluation_sessions"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False) # e.g. "2025 Regular Evaluation"
    start_date = Column(Date, nullable=False)
    status = Column(String, default="DRAFT") # DRAFT, ACTIVE, CLOSED
    
    evaluations = relationship("JobEvaluation", back_populates="session")

class JobEvaluationCriteria(Base):
    """
    Evaluation Factors (e.g. Knowledge, Complexity, Impact)
    """
    __tablename__ = "job_evaluation_criteria"
    id = Column(String, primary_key=True, default=generate_uuid)
    category = Column(String, nullable=False) # Input, Process, Output
    name = Column(String, nullable=False)
    weight = Column(Float, default=1.0)
    description = Column(Text, nullable=True)

class JobEvaluation(Base):
    """
    The act of evaluating a Job.
    """
    __tablename__ = "job_evaluations"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_id = Column(String, ForeignKey("job_positions.id"))
    session_id = Column(String, ForeignKey("evaluation_sessions.id"), nullable=True)
    
    # Scores
    total_score = Column(Float, default=0.0)
    final_grade = Column(Enum(JobGrade), nullable=True)
    
    # Hybrid Logic: AI Suggestion vs Human Decision
    ai_suggested_grade = Column(Enum(JobGrade), nullable=True)
    evaluator_comment = Column(Text, nullable=True)
    
    job = relationship("JobPosition")
    session = relationship("EvaluationSession", back_populates="evaluations")
    scores = relationship("JobEvaluationScore", back_populates="evaluation")

class JobEvaluationScore(Base):
    """
    Detailed granular scores per criteria.
    """
    __tablename__ = "job_evaluation_scores"
    id = Column(String, primary_key=True, default=generate_uuid)
    evaluation_id = Column(String, ForeignKey("job_evaluations.id"))
    criteria_id = Column(String, ForeignKey("job_evaluation_criteria.id"))
    
    score = Column(Float, default=0.0) # The actual score given
    
    evaluation = relationship("JobEvaluation", back_populates="scores")
    criteria = relationship("JobEvaluationCriteria")
