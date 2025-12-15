from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..database import get_db
from ..models import JobTask, JobPosition, JobDescription, User
from ..services.search_engine import TFIDFEngine
from ..services.jd_generator import TemplateJDGenerator
from ..services.gap_analysis import SmartWorkloadAnalyzer

router = APIRouter(
    prefix="/ai",
    tags=["AI Intelligence"],
)

# Global Engine Instance
search_engine = TFIDFEngine()
jd_generator = TemplateJDGenerator()
gap_analyzer = SmartWorkloadAnalyzer()
is_indexed = False

class SearchResult(BaseModel):
    id: str
    type: str # 'job', 'task', 'person'
    title: str
    description: str
    score: float

def ensure_index(db: Session):
    global is_indexed
    if is_indexed:
        return
        
    # Index Job Tasks
    tasks = db.query(JobTask).all()
    for t in tasks:
        # Combo text: Name + Verb
        text = f"{t.task_name} {t.action_verb}"
        search_engine.add_document(f"task:{t.id}", text)
        
    # Index Positions (Titles)
    positions = db.query(JobPosition).all()
    for p in positions:
        search_engine.add_document(f"position:{p.id}", p.title)

    # Index Job Descriptions
    jds = db.query(JobDescription).all()
    for jd in jds:
        # Rich text: Overview + Responsibilities + Qualifications
        text = f"{jd.overview} {jd.responsibilities} {jd.qualifications}"
        search_engine.add_document(f"jd:{jd.job_id}", text)
        
    search_engine.build_index()
    is_indexed = True

@router.get("/search", response_model=List[SearchResult])
def semantic_search(
    query: str, 
    type: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    if not query:
        return []
        
    ensure_index(db)
    
    # Get raw results from engine (IDs)
    raw_results = search_engine.search(query, top_k=20)
    
    results = []
    
    # Enrich results with DB data
    for doc_id, score in raw_results:
        prefix, db_id = doc_id.split(":", 1)
        
        # Filter by type if requested
        if type and type != 'all' and prefix != type:
            continue
            
        try:
            item = None
            if prefix == "task":
                obj = db.query(JobTask).filter(JobTask.id == db_id).first()
                if obj:
                    item = SearchResult(
                        id=obj.id, 
                        type="Task", 
                        title=obj.task_name, 
                        description=f"Action: {obj.action_verb}", 
                        score=score
                    )
            elif prefix == "position":
                obj = db.query(JobPosition).filter(JobPosition.id == db_id).first()
                if obj:
                    item = SearchResult(
                        id=obj.id, 
                        type="Position", 
                        title=obj.title, 
                        description=f"Grade: {obj.grade}", 
                        score=score
                    )
            elif prefix == "jd":
                # For JD, we usually link to the Position
                obj = db.query(JobPosition).filter(JobPosition.id == db_id).first()
                jd_obj = db.query(JobDescription).filter(JobDescription.job_id == db_id).first()
                if obj and jd_obj:
                    item = SearchResult(
                        id=obj.id, 
                        type="Job Description", 
                        title=f"JD: {obj.title}", 
                        description=jd_obj.overview[:100] + "...", 
                        score=score
                    )

            if item:
                results.append(item)
                
        except Exception as e:
            print(f"Error enriching {doc_id}: {e}")
            continue

    return results[:10]

# --- JD Generator ---
class GenerateJDRequest(BaseModel):
    position_id: str
    task_ids: List[str]

@router.post("/generate-jd")
def generate_job_description(req: GenerateJDRequest, db: Session = Depends(get_db)):
    # 1. Fetch Position
    position = db.query(JobPosition).filter(JobPosition.id == req.position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
        
    # 2. Fetch Tasks (names and verbs)
    tasks_data = []
    for tid in req.task_ids:
        task = db.query(JobTask).filter(JobTask.id == tid).first()
        if task:
            tasks_data.append({"task_name": task.task_name, "action_verb": task.action_verb})
            
    if not tasks_data:
        raise HTTPException(status_code=400, detail="No valid tasks found")

    # 3. Generate
    result = jd_generator.generate(
        position_title=position.title,
        position_grade=position.grade or "G3", # fallback
        tasks=tasks_data
    )
    
    return result

# --- Smart Gap Analysis ---
class AnalyzeWorkloadRequest(BaseModel):
    tasks: List[dict] # Expected: [{'task_name': str, 'fte': float, 'action_verb': str}]

@router.post("/analyze-workload")
def analyze_workload_gap(req: AnalyzeWorkloadRequest):
    if not req.tasks:
        raise HTTPException(status_code=400, detail="No tasks provided")
        
    analysis = gap_analyzer.cluster_tasks(req.tasks)
    return analysis
