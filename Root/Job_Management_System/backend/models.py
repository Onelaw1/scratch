from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, Text, Enum, Date, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import uuid
import enum

def generate_uuid():
    return str(uuid.uuid4())

# --- Enums ---
class InstitutionCategory(str, enum.Enum):
    MARKET = "MARKET"
    QUASI_MARKET = "QUASI_MARKET"
    FUND = "FUND"
    CONSIGNMENT = "CONSIGNMENT"

class UnitType(str, enum.Enum):
    HQ = "HQ"          # 본부
    OFFICE = "OFFICE"  # 실
    TEAM = "TEAM"      # 팀

class JobGrade(str, enum.Enum):
    G1 = "G1"
    G2 = "G2"
    G3 = "G3"
    G4 = "G4"
    G5 = "G5"

class SurveyStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

class DependencyType(str, enum.Enum):
    BLOCKS = "BLOCKS"
    RELATED = "RELATED"
    SEQUENTIAL = "SEQUENTIAL"

class TaskFrequency(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    SEASONAL = "SEASONAL"
    IRREGULAR = "IRREGULAR"

class RaterType(str, enum.Enum):
    SELF = "SELF"
    PEER = "PEER"
    SUPERVISOR_1 = "SUPERVISOR_1" # Direct
    SUPERVISOR_2 = "SUPERVISOR_2" # Next Level
    EXTERNAL = "EXTERNAL" # Committee

class ReviewStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    FINAL = "FINAL"

class TrainingStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

# --- Core Models ---
class Institution(Base):
    __tablename__ = "institutions"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    category = Column(Enum(InstitutionCategory), nullable=True)
    
    org_units = relationship("OrgUnit", back_populates="institution")
    users = relationship("User", back_populates="institution")
    benchmark_data = relationship("ExternalBenchmarkData", back_populates="institution")
    strategic_analyses = relationship("StrategicAnalysis", back_populates="institution")
    headcount_plans = relationship("HeadcountPlan", back_populates="institution")
    financial_performance = relationship("FinancialPerformance", back_populates="institution")

class OrgUnit(Base):
    __tablename__ = "org_units"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    parent_id = Column(String, ForeignKey("org_units.id"), nullable=True)
    name = Column(String, nullable=False)
    unit_type = Column(Enum(UnitType), nullable=False)
    mission = Column(Text, nullable=True) # For Cascading
    
    # ERP Synced Fields
    budget = Column(Float, default=0.0)
    authorized_headcount = Column(Float, default=0.0)
    
    institution = relationship("Institution", back_populates="org_units")
    parent = relationship("OrgUnit", remote_side=[id], backref="children")
    users = relationship("User", back_populates="org_unit")
    team_budgets = relationship("TeamBudget", back_populates="org_unit")

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    org_unit_id = Column(String, ForeignKey("org_units.id"))
    reports_to_id = Column(String, ForeignKey("users.id"), nullable=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hire_date = Column(Date, nullable=True)
    
    # 2.7 Personnel Card Details
    birth_date = Column(Date, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    education_level = Column(String, nullable=True) # e.g., Bachelor, Master
    certifications = Column(JSON, nullable=True) # List of certifications
    career_history = Column(JSON, nullable=True) # List of previous jobs
    current_salary = Column(Float, default=50000000.0) # Mock Salary
    gender = Column(String, default="Male") # Male, Female
    
    institution = relationship("Institution", back_populates="users")
    org_unit = relationship("OrgUnit", back_populates="users")
    job_positions = relationship("JobPosition", back_populates="user")
    reviews = relationship("PerformanceReview", back_populates="user")
    workload_entries = relationship("WorkloadEntry", back_populates="user")
    trainings = relationship("EmployeeTraining", back_populates="user")
    promotion_entries = relationship("PromotionList", back_populates="user")
    career_goals = relationship("CareerGoal", back_populates="user")
    
    reports_to = relationship("User", remote_side=[id], backref="direct_reports")
    competencies = relationship("UserCompetency", back_populates="user")

# --- Strategic Analysis ---
class StrategicAnalysis(Base):
    __tablename__ = "strategic_analyses"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    analysis_type = Column(String, nullable=False) # PEST, SWOT, etc.
    content = Column(Text, nullable=False) # JSON string
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    institution = relationship("Institution", back_populates="strategic_analyses")

# --- Job Architecture (2.2 Job Classification) ---
class JobGroup(Base):
    __tablename__ = "job_groups"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    series = relationship("JobSeries", back_populates="group")

class JobSeries(Base):
    __tablename__ = "job_series"
    id = Column(String, primary_key=True, default=generate_uuid)
    group_id = Column(String, ForeignKey("job_groups.id"))
    name = Column(String, nullable=False)
    
    # 2.2 NCS Mapping
    ncs_code = Column(String, nullable=True) # Primary NCS Code
    ncs_name = Column(String, nullable=True)
    
    group = relationship("JobGroup", back_populates="series")
    positions = relationship("JobPosition", back_populates="series")
    training_programs = relationship("TrainingProgram", back_populates="series")

# --- 2.11 Job Redesign (Simulation) ---
class SimulationScenario(Base):
    __tablename__ = "simulation_scenarios"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    positions = relationship("JobPosition", back_populates="scenario")

class JobPosition(Base):
    __tablename__ = "job_positions"
    id = Column(String, primary_key=True, default=generate_uuid)
    series_id = Column(String, ForeignKey("job_series.id"))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    scenario_id = Column(String, ForeignKey("simulation_scenarios.id"), nullable=True) # If null, it's LIVE data
    
    title = Column(String, nullable=False)
    grade = Column(Enum(JobGrade), nullable=True)
    is_future_model = Column(Boolean, default=False)
    assignment_date = Column(Date, nullable=True) # For Job Tenure Tracking
    
    series = relationship("JobSeries", back_populates="positions")
    user = relationship("User", back_populates="job_positions")
    scenario = relationship("SimulationScenario", back_populates="positions")
    
    tasks = relationship("JobTask", back_populates="position", cascade="all, delete-orphan") # Added cascade for easy cleanup
    evaluation = relationship("JobEvaluation", uselist=False, back_populates="position", cascade="all, delete-orphan")
    descriptions = relationship("JobDescription", back_populates="position")
    required_competencies = relationship("JobCompetency", back_populates="position")
    history = relationship("JobHistory", back_populates="position")

class JobTask(Base):
    __tablename__ = "job_tasks"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_position_id = Column(String, ForeignKey("job_positions.id"))
    task_name = Column(String, nullable=False)
    action_verb = Column(String, nullable=True)
    task_object = Column(String, nullable=True)
    
    # AI Impact Analysis
    ai_substitution = Column(Float, default=0.0)
    ai_augmentation = Column(Float, default=0.0)
    ai_generation = Column(Float, default=0.0)
    
    position = relationship("JobPosition", back_populates="tasks")
    work_items = relationship("WorkItem", back_populates="task")
    workload_entries = relationship("WorkloadEntry", back_populates="task")
    next_tasks = relationship("TaskDependency", foreign_keys="[TaskDependency.source_task_id]", back_populates="source_task")
    prev_tasks = relationship("TaskDependency", foreign_keys="[TaskDependency.target_task_id]", back_populates="target_task")

# --- 2.12 Competency Model ---
class Competency(Base):
    __tablename__ = "competencies"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True) # e.g. Technical, Leadership
    
    job_links = relationship("JobCompetency", back_populates="competency")
    user_links = relationship("UserCompetency", back_populates="competency")

class JobCompetency(Base):
    __tablename__ = "job_competencies"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_position_id = Column(String, ForeignKey("job_positions.id"))
    competency_id = Column(String, ForeignKey("competencies.id"))
    required_level = Column(Integer, default=1) # 1-5
    weight = Column(Float, default=1.0)
    
    position = relationship("JobPosition", back_populates="required_competencies")
    competency = relationship("Competency", back_populates="job_links")

class UserCompetency(Base):
    __tablename__ = "user_competencies"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    competency_id = Column(String, ForeignKey("competencies.id"))
    current_level = Column(Integer, default=1) # 1-5
    evaluated_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="competencies")
    competency = relationship("Competency", back_populates="user_links")

# --- 2.9 Job Management Card (History) ---
class JobHistory(Base):
    __tablename__ = "job_histories"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_position_id = Column(String, ForeignKey("job_positions.id"))
    change_date = Column(Date, default=func.now())
    change_type = Column(String, nullable=False) # e.g., "GRADE_CHANGE", "TASK_UPDATE"
    description = Column(String, nullable=True)
    
    position = relationship("JobPosition", back_populates="history")

# --- 2.1 Workforce Planning & 2.5 Workload Survey ---
class CareerGoalStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class CareerGoal(Base):
    __tablename__ = "career_goals"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    deadline = Column(Date, nullable=True)
    status = Column(Enum(CareerGoalStatus), default=CareerGoalStatus.NOT_STARTED)
    
    user = relationship("User", back_populates="career_goals")

# --- Employee Experience (Pulse) ---
class PulseWorkloadLevel(str, enum.Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    OVERLOAD = "OVERLOAD"

class DailyPulse(Base):
    __tablename__ = "daily_pulses"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    mood_score = Column(Integer) # 1-5
    workload_level = Column(Enum(PulseWorkloadLevel))
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")

class SurveyPeriod(Base):
    __tablename__ = "survey_periods"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(Enum(SurveyStatus), default=SurveyStatus.DRAFT)
    
    entries = relationship("WorkloadEntry", back_populates="survey_period")

class WorkItem(Base):
    __tablename__ = "work_items"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_task_id = Column(String, ForeignKey("job_tasks.id"))
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    frequency = Column(Enum(TaskFrequency), nullable=True)
    seasonal_details = Column(String, nullable=True)
    estimated_hours_per_occurrence = Column(Float, default=0.0)
    workload_amount = Column(Float, default=0.0)
    
    task = relationship("JobTask", back_populates="work_items")

class WorkloadEntry(Base):
    __tablename__ = "workload_entries"
    id = Column(String, primary_key=True, default=generate_uuid)
    survey_period_id = Column(String, ForeignKey("survey_periods.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"))
    task_id = Column(String, ForeignKey("job_tasks.id"))
    
    volume = Column(Float, default=0.0) # Frequency
    standard_time = Column(Float, default=0.0) # Hours
    fte = Column(Float, default=0.0) # Calculated
    
    survey_period = relationship("SurveyPeriod", back_populates="entries")
    user = relationship("User", back_populates="workload_entries")
    task = relationship("JobTask", back_populates="workload_entries")

# --- 2.10 Headcount Management ---
class HeadcountPlan(Base):
    __tablename__ = "headcount_plans"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    year = Column(Integer, nullable=False)
    org_unit_id = Column(String, ForeignKey("org_units.id"), nullable=True)
    
    authorized_count = Column(Float, default=0.0) # 정원
    current_count = Column(Float, default=0.0) # 현원
    required_count = Column(Float, default=0.0) # 적정인력 (Calculated)
    
    institution = relationship("Institution", back_populates="headcount_plans")

# --- External Benchmark ---
class ExternalBenchmarkData(Base):
    __tablename__ = "external_benchmark_data"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"), nullable=True)
    institution_type = Column(String, nullable=True) # e.g. "Public Corp"
    headcount_range = Column(String, nullable=True) # e.g. "100-300"
    budget_range = Column(String, nullable=True) # e.g. "100B-300B"
    
    avg_hcroi = Column(Float, default=0.0) # Human Capital ROI
    avg_hcva = Column(Float, default=0.0) # Human Capital Value Added
    
    institution = relationship("Institution", back_populates="benchmark_data")

class FinancialPerformance(Base):
    __tablename__ = "financial_performance"
    id = Column(String, primary_key=True, default=generate_uuid)
    institution_id = Column(String, ForeignKey("institutions.id"))
    year = Column(Integer, nullable=False)
    
    revenue = Column(Float, default=0.0) # Total Revenue (매출액)
    operating_expenses = Column(Float, default=0.0) # Excluding Personnel (인건비 제외 운영비용)
    personnel_costs = Column(Float, default=0.0) # Total Personnel Costs (총 인건비)
    
    # Pre-calculated Metrics (Optional, as they can be computed on fly)
    net_income = Column(Float, default=0.0) # Revenue - (OpEx + Personnel)
    
    institution = relationship("Institution", back_populates="financial_performance")

class TeamBudget(Base):
    __tablename__ = "team_budgets"
    id = Column(String, primary_key=True, default=generate_uuid)
    org_unit_id = Column(String, ForeignKey("org_units.id"))
    year = Column(Integer, nullable=False)
    amount = Column(Float, default=0.0)
    
    org_unit = relationship("OrgUnit", back_populates="team_budgets")

# --- Workflow & Process ---
class TaskDependency(Base):
    __tablename__ = "task_dependencies"
    id = Column(String, primary_key=True, default=generate_uuid)
    source_task_id = Column(String, ForeignKey("job_tasks.id"))
    target_task_id = Column(String, ForeignKey("job_tasks.id"))
    dependency_type = Column(Enum(DependencyType), default=DependencyType.SEQUENTIAL)
    description = Column(String, nullable=True)
    
    source_task = relationship("JobTask", foreign_keys=[source_task_id], back_populates="next_tasks")
    target_task = relationship("JobTask", foreign_keys=[target_task_id], back_populates="prev_tasks")

# --- 2.8 Job Evaluation ---
class JobEvaluation(Base):
    __tablename__ = "job_evaluations"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_position_id = Column(String, ForeignKey("job_positions.id"))
    score_expertise = Column(Float, default=0.0)
    score_responsibility = Column(Float, default=0.0)
    score_complexity = Column(Float, default=0.0)
    total_score = Column(Float, default=0.0)
    grade = Column(Enum(JobGrade), nullable=True)
    
    position = relationship("JobPosition", back_populates="evaluation")
    scores = relationship("JobEvaluationScore", back_populates="evaluation")

class JobEvaluationScore(Base):
    __tablename__ = "job_evaluation_scores"
    id = Column(String, primary_key=True, default=generate_uuid)
    evaluation_id = Column(String, ForeignKey("job_evaluations.id"))
    rater_type = Column(Enum(RaterType), nullable=False)
    rater_user_id = Column(String, ForeignKey("users.id"), nullable=True) # Null for external
    
    score_expertise = Column(Float, default=0.0)
    score_responsibility = Column(Float, default=0.0)
    score_complexity = Column(Float, default=0.0)
    raw_total = Column(Float, default=0.0)
    
    # Bias Prevention
    z_score = Column(Float, default=0.0) # Statistical Normalization
    final_score = Column(Float, default=0.0) # After weighting
    
    evaluation = relationship("JobEvaluation", back_populates="scores")

# --- 2.3 Job Description ---
class JobDescription(Base):
    __tablename__ = "job_descriptions"
    id = Column(String, primary_key=True, default=generate_uuid)
    job_position_id = Column(String, ForeignKey("job_positions.id"))
    summary = Column(Text, nullable=True)
    qualification_requirements = Column(Text, nullable=True)
    kpi_indicators = Column(Text, nullable=True)
    version = Column(Integer, default=1)
    
    position = relationship("JobPosition", back_populates="descriptions")

# --- 2.6 Performance Evaluation ---
class PerformanceReview(Base):
    __tablename__ = "performance_reviews"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    year = Column(Integer, nullable=False)
    status = Column(Enum(ReviewStatus), default=ReviewStatus.DRAFT)
    review_date = Column(Date, nullable=True)
    
    score_common = Column(Float, default=0.0) # Common Competency
    score_leadership = Column(Float, default=0.0) # Leadership
    score_job = Column(Float, default=0.0) # Job Performance (Calculated from Goals)
    score_potential = Column(Float, default=0.0) # Potential Score
    potential_grade = Column(String, nullable=True) # High, Mod, Low
    nine_box_position = Column(Integer, nullable=True) # 1-9
    total_score = Column(Float, default=0.0)
    grade = Column(String, nullable=True) # S, A, B, C, D
    
    user = relationship("User", back_populates="reviews")
    goals = relationship("PerformanceGoal", back_populates="review")

class PerformanceGoal(Base):
    __tablename__ = "performance_goals"
    id = Column(String, primary_key=True, default=generate_uuid)
    review_id = Column(String, ForeignKey("performance_reviews.id"))
    category = Column(String, nullable=False) # e.g. "MBO", "BSC_FINANCIAL"
    goal_text = Column(Text, nullable=False)
    weight = Column(Float, default=0.0) # Percentage (0-100)
    target = Column(Text, nullable=True)
    actual = Column(Text, nullable=True)
    
    self_score = Column(Float, default=0.0)
    supervisor_score = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    
    review = relationship("PerformanceReview", back_populates="goals")

# --- 2.4 Promotion System ---
class PromotionList(Base):
    __tablename__ = "promotion_lists"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    target_grade = Column(Enum(JobGrade), nullable=False)
    rank = Column(Integer, nullable=False)
    total_points = Column(Float, default=0.0)
    
    # Detailed Scoring
    score_performance = Column(Float, default=0.0)
    score_experience = Column(Float, default=0.0)
    score_language = Column(Float, default=0.0)
    score_training = Column(Float, default=0.0)
    
    user = relationship("User", back_populates="promotion_entries")

# --- 3. Enterprise Integration (ERP) ---
class ERPSyncLog(Base):
    __tablename__ = "erp_sync_logs"
    id = Column(String, primary_key=True, default=generate_uuid)
    sync_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, nullable=False) # SUCCESS, FAILED
    records_updated = Column(Integer, default=0)
    details = Column(Text, nullable=True) # JSON log of changes
    
    institution_id = Column(String, ForeignKey("institutions.id"))

class TrainingProgram(Base):
    __tablename__ = "training_programs"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    duration_hours = Column(Float, default=0.0)
    target_job_series_id = Column(String, ForeignKey("job_series.id"), nullable=True)
    required_competency = Column(String, nullable=True)
    
    series = relationship("JobSeries", back_populates="training_programs")
    attendees = relationship("EmployeeTraining", back_populates="program")

class EmployeeTraining(Base):
    __tablename__ = "employee_trainings"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"))
    program_id = Column(String, ForeignKey("training_programs.id"))
    status = Column(Enum(TrainingStatus), default=TrainingStatus.PLANNED)
    completion_date = Column(Date, nullable=True)
    score = Column(Float, nullable=True)
    
    user = relationship("User", back_populates="trainings")
    program = relationship("TrainingProgram", back_populates="attendees")
