"""
Job Data Extractor Service
Extracts and transforms data from Job Management System database for PPT generation.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Dict, List, Optional
import sys
import os

# Add Job Management System root to path
root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Job_Management_System')
sys.path.append(root_path)

try:
    from backend.models import (
        JobGroup, JobSeries, JobPosition, JobTaskNew, WorkItem,
        OrganizationalUnit, User, Institution, StrategicAnalysis
    )
except ImportError as e:
    print(f"Warning: Could not import Job Management System models: {e}")


class JobDataExtractor:
    """Extract data from Job Management System database"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize data extractor
        
        Args:
            db_path: Path to SQLite database (default: Job_Management_System/sql_app.db)
        """
        if db_path is None:
            # Default path
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            db_path = os.path.join(base_dir, '..', 'Job_Management_System', 'sql_app.db')
        
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        SessionLocal = sessionmaker(bind=self.engine)
        self.session = SessionLocal()
    
    def get_org_hierarchy(self) -> Dict:
        """
        Extract organizational hierarchy for org chart
        
        Returns:
            Dict with CEO and C-Level structure
        """
        try:
            # Get organizational units
            units = self.session.query(OrganizationalUnit).all()
            
            # Build hierarchy
            hierarchy = {
                "CEO": "CEO",
                "C-Level": []
            }
            
            for unit in units:
                if unit.parent_id is None:
                    # Top-level unit
                    hierarchy["C-Level"].append(f"{unit.name} ({unit.code})")
            
            return hierarchy
        except Exception as e:
            print(f"Error extracting org hierarchy: {e}")
            return {"CEO": "CEO", "C-Level": ["CFO", "CTO", "CMO"]}
    
    def get_fte_by_department(self) -> Dict[str, Dict[str, float]]:
        """
        Extract FTE data by department
        
        Returns:
            Dict mapping department names to current/required FTE
        """
        try:
            units = self.session.query(OrganizationalUnit).all()
            
            fte_data = {}
            for unit in units:
                # Calculate current FTE (headcount)
                current = float(unit.headcount) if unit.headcount else 0.0
                
                # Estimate required FTE (for demo, use 120% of current)
                required = current * 1.2
                
                fte_data[unit.name] = {
                    "current": current,
                    "required": required
                }
            
            return fte_data
        except Exception as e:
            print(f"Error extracting FTE data: {e}")
            return {
                "Engineering": {"current": 10.0, "required": 15.0},
                "Sales": {"current": 8.0, "required": 8.0}
            }
    
    def get_job_tasks_matrix(self) -> Dict[str, Dict[str, str]]:
        """
        Extract job tasks for RACI matrix
        
        Returns:
            Dict mapping task names to role assignments
        """
        try:
            tasks = self.session.query(JobTaskNew).limit(10).all()
            
            raci_data = {}
            for task in tasks:
                # Simplified RACI assignment
                raci_data[task.name] = {
                    "PM": "A",
                    "Dev": "R",
                    "QA": "C",
                    "Ops": "I"
                }
            
            return raci_data
        except Exception as e:
            print(f"Error extracting RACI data: {e}")
            return {
                "Task 1": {"PM": "R", "Dev": "C", "QA": "I", "Ops": "I"},
                "Task 2": {"PM": "A", "Dev": "R", "QA": "C", "Ops": "I"}
            }
    
    def get_workload_stats(self) -> Dict:
        """
        Extract workload statistics
        
        Returns:
            Dict with workload distribution data
        """
        try:
            positions = self.session.query(JobPosition).all()
            
            stats = {
                "total_positions": len(positions),
                "by_grade": {},
                "by_series": {}
            }
            
            for pos in positions:
                # Count by grade
                grade = pos.current_grade or "Unknown"
                stats["by_grade"][grade] = stats["by_grade"].get(grade, 0) + 1
            
            return stats
        except Exception as e:
            print(f"Error extracting workload stats: {e}")
            return {"total_positions": 0, "by_grade": {}, "by_series": {}}
    
    def get_grade_distribution(self) -> Dict[str, int]:
        """
        Extract grade distribution for analysis
        
        Returns:
            Dict mapping grade levels to counts
        """
        try:
            positions = self.session.query(JobPosition).all()
            
            distribution = {}
            for pos in positions:
                grade = pos.current_grade or "Unknown"
                distribution[grade] = distribution.get(grade, 0) + 1
            
            return distribution
            return distribution
        except Exception as e:
            print(f"Error extracting grade distribution: {e}")
            return {"Grade 5": 10, "Grade 4": 15, "Grade 3": 20}
    
    def get_strategic_analysis(self, institution_id: str, analysis_type: str) -> Dict:
        """
        Extract strategic analysis data (SWOT, 4P, etc.)
        
        Args:
            institution_id: ID of the institution
            analysis_type: Type of analysis (SWOT, FOUR_P, etc.)
            
        Returns:
            Dict containing the analysis data
        """
        try:
            import json
            analysis = self.session.query(StrategicAnalysis).filter(
                StrategicAnalysis.institution_id == institution_id,
                StrategicAnalysis.analysis_type == analysis_type
            ).order_by(StrategicAnalysis.created_at.desc()).first()
            
            if analysis and analysis.content:
                return json.loads(analysis.content)
            return {}
        except Exception as e:
            print(f"Error extracting strategic analysis ({analysis_type}): {e}")
            return {}
    
    def close(self):
        """Close database session"""
        self.session.close()
