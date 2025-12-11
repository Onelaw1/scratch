
schema_code = """
# --- Missing Strategic Analysis Schemas ---

class StrategicAnalysisBase(BaseModel):
    institution_id: str
    analysis_type: str
    content: str # JSON string

class StrategicAnalysisCreate(StrategicAnalysisBase):
    pass

class StrategicAnalysis(StrategicAnalysisBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
"""

with open("c:/Users/Administrator/Downloads/Root/Job_Management_System/backend/schemas.py", "a") as f:
    f.write(schema_code)
print("StrategicAnalysis schemas appended successfully.")
