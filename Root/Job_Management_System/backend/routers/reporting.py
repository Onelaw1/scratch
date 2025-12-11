from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import shutil
import os
import uuid
from typing import Optional
import sys

# Add PPT Agent to path to import services
# Add PPT Agent to path to import services
ppt_agent_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'PPT_Agent')
sys.path.append(ppt_agent_path)

from src.services.data_ingestion_service import DataIngestionService
from src.services.pptx_service import PPTXService
from src.models.schema import PresentationSchema, SlideContent

router = APIRouter(
    prefix="/api/reporting",
    tags=["reporting"],
)

ingestion_service = DataIngestionService()
pptx_service = PPTXService(output_dir=os.path.join(ppt_agent_path, "output", "web_reports"))

@router.post("/generate")
async def generate_report(
    file: UploadFile = File(...),
    framework_type: str = Form(...),
    title: str = Form("Strategic Report")
):
    """
    Generate a PPT report from an uploaded file (Excel or Image).
    """
    try:
        # Save uploaded file temporarily
        temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
        temp_path = os.path.join(ppt_agent_path, "output", "temp", temp_filename)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Determine source type
        filename = file.filename.lower()
        source_type = "dict"
        if filename.endswith(('.xlsx', '.xls')):
            source_type = "excel"
        elif filename.endswith(('.png', '.jpg', '.jpeg')):
            source_type = "image"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
            
        # Ingest Data
        print(f"Ingesting data from {source_type} file: {temp_path}")
        data = ingestion_service.ingest_data(temp_path, source_type)
        
        if not data:
            raise HTTPException(status_code=400, detail="Failed to extract data from file")
            
        # Create Presentation Schema
        slides = [
            SlideContent(
                title=f"{framework_type.upper()} Analysis", 
                bullet_points=["Generated from uploaded file"]
            )
        ]
        schema = PresentationSchema(topic=title, slides=slides)
        
        # Create Design Schema
        design_schema = [
            {
                "diagram_type": framework_type,
                "diagram_data": data
            }
        ]
        
        # Generate PPT
        output_filename = f"report_{uuid.uuid4()}.pptx"
        output_path = pptx_service.create_presentation(
            schema, 
            filename=output_filename, 
            design_schema=design_schema
        )
        
        # Cleanup temp file
        os.remove(temp_path)
        
        return FileResponse(
            output_path, 
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", 
            filename=f"{title}.pptx"
        )
        
    except Exception as e:
        print(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
