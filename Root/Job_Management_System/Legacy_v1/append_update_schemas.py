
schema_code = """
# --- Missing Update Schemas ---

class JobGroupUpdate(BaseModel):
    name: Optional[str] = None

class JobSeriesUpdate(BaseModel):
    name: Optional[str] = None
    ncs_code: Optional[str] = None
    ncs_name: Optional[str] = None

class JobPositionUpdate(BaseModel):
    title: Optional[str] = None
    grade: Optional[JobGrade] = None
    is_future_model: Optional[bool] = None

class JobTaskUpdate(BaseModel):
    task_name: Optional[str] = None
    action_verb: Optional[str] = None
    task_object: Optional[str] = None
    ai_substitution: Optional[float] = None
    ai_augmentation: Optional[float] = None
    ai_generation: Optional[float] = None

class WorkItemUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[TaskFrequency] = None
    seasonal_details: Optional[str] = None
    estimated_hours_per_occurrence: Optional[float] = None
    workload_amount: Optional[float] = None

class StrategicAnalysisUpdate(BaseModel):
    analysis_type: Optional[str] = None
    content: Optional[str] = None
"""

with open("c:/Users/Administrator/Downloads/Root/Job_Management_System/backend/schemas.py", "a") as f:
    f.write(schema_code)
print("Update schemas appended successfully.")
