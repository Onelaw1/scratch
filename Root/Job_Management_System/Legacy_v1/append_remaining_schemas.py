
schema_code = """
# --- Missing Job Evaluation Schemas ---

class JobEvaluationScoreBase(BaseModel):
    rater_type: RaterType
    score_expertise: float
    score_responsibility: float
    score_complexity: float
    rater_user_id: Optional[str] = None

class JobEvaluationScoreCreate(JobEvaluationScoreBase):
    evaluation_id: Optional[str] = None

class JobEvaluationScore(JobEvaluationScoreBase):
    id: str
    evaluation_id: str
    raw_total: float
    z_score: float
    final_score: float

    class Config:
        from_attributes = True

class JobEvaluationBase(BaseModel):
    job_position_id: str
    grade: Optional[JobGrade] = None

class JobEvaluationCreate(JobEvaluationBase):
    pass

class JobEvaluation(JobEvaluationBase):
    id: str
    total_score: float
    scores: List[JobEvaluationScore] = []

    class Config:
        from_attributes = True

# --- Missing Performance Review Schemas ---

class PerformanceGoalBase(BaseModel):
    category: str
    goal_text: str
    weight: float
    target: Optional[str] = None
    actual: Optional[str] = None
    self_score: float = 0.0
    supervisor_score: float = 0.0

class PerformanceGoalCreate(PerformanceGoalBase):
    review_id: Optional[str] = None

class PerformanceGoalUpdate(BaseModel):
    category: Optional[str] = None
    goal_text: Optional[str] = None
    weight: Optional[float] = None
    target: Optional[str] = None
    actual: Optional[str] = None
    self_score: Optional[float] = None
    supervisor_score: Optional[float] = None
    final_score: Optional[float] = None

class PerformanceGoal(PerformanceGoalBase):
    id: str
    review_id: str
    final_score: float

    class Config:
        from_attributes = True

class PerformanceReviewBase(BaseModel):
    user_id: str
    year: int
    status: ReviewStatus = ReviewStatus.DRAFT
    review_date: Optional[date] = None
    score_common: float = 0.0
    score_leadership: float = 0.0

class PerformanceReviewCreate(PerformanceReviewBase):
    pass

class PerformanceReviewUpdate(BaseModel):
    status: Optional[ReviewStatus] = None
    review_date: Optional[date] = None
    score_common: Optional[float] = None
    score_leadership: Optional[float] = None
    score_job: Optional[float] = None
    total_score: Optional[float] = None
    grade: Optional[str] = None

class PerformanceReview(PerformanceReviewBase):
    id: str
    score_job: float
    total_score: float
    grade: Optional[str] = None
    goals: List[PerformanceGoal] = []

    class Config:
        from_attributes = True

# --- Missing Training Schemas ---

class TrainingProgramBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration_hours: float = 0.0
    target_job_series_id: Optional[str] = None
    required_competency: Optional[str] = None

class TrainingProgramCreate(TrainingProgramBase):
    pass

class TrainingProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_hours: Optional[float] = None
    target_job_series_id: Optional[str] = None
    required_competency: Optional[str] = None

class TrainingProgram(TrainingProgramBase):
    id: str

    class Config:
        from_attributes = True

class EmployeeTrainingBase(BaseModel):
    user_id: str
    program_id: str
    status: TrainingStatus = TrainingStatus.PLANNED
    completion_date: Optional[date] = None
    score: Optional[float] = None

class EmployeeTrainingCreate(EmployeeTrainingBase):
    pass

class EmployeeTrainingUpdate(BaseModel):
    status: Optional[TrainingStatus] = None
    completion_date: Optional[date] = None
    score: Optional[float] = None

class EmployeeTraining(EmployeeTrainingBase):
    id: str
    # program: TrainingProgram # Forward ref issue, omitting for now

    class Config:
        from_attributes = True

# --- Missing Promotion Schemas ---

class PromotionListBase(BaseModel):
    target_grade: JobGrade
    rank: int
    total_points: float
    score_performance: float = 0.0
    score_experience: float = 0.0
    score_language: float = 0.0
    score_training: float = 0.0

class PromotionListCreate(PromotionListBase):
    user_id: str

class PromotionList(PromotionListBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True
"""

with open("c:/Users/Administrator/Downloads/Root/Job_Management_System/backend/schemas.py", "a") as f:
    f.write(schema_code)
print("Remaining schemas appended successfully.")
