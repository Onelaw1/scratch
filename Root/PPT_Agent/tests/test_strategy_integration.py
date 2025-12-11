import os
import sys
import json
import uuid
from datetime import datetime

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.services.pptx_service import PPTXService
from src.models.schema import PresentationSchema, SlideContent
from src.services.job_data_extractor import JobDataExtractor
from backend.models import StrategicAnalysis, Institution, AnalysisType
from backend.database import SessionLocal

def test_hybrid_strategy_integration():
    print("Testing Hybrid Strategy Integration...")
    
    # 1. Setup Data
    # Use JobDataExtractor's session to ensure we hit the correct DB
    extractor = JobDataExtractor()
    db = extractor.session
    
    # Create a dummy institution for DB test
    inst_id = str(uuid.uuid4())
    inst = Institution(
        id=inst_id,
        name="Test Corp",
        code=f"TEST_{inst_id[:8]}",
        category_type="MARKET",
        evaluation_group="SERVICE"
    )
    db.add(inst)
    
    # Create a SWOT analysis in DB
    swot_data = {
        "strengths": ["Strong Brand", "Global Presence"],
        "weaknesses": ["High Cost", "Slow Innovation"],
        "opportunities": ["Emerging Markets", "AI Adoption"],
        "threats": ["Competitors", "Regulations"]
    }
    analysis = StrategicAnalysis(
        institution_id=inst_id,
        analysis_type="SWOT",
        title="2024 Strategic SWOT",
        content=json.dumps(swot_data)
    )
    db.add(analysis)
    db.commit()
    print(f"Inserted DB Data for Institution: {inst_id}")
    
    # 2. Define Presentation Schema
    slides = [
        SlideContent(title="Direct Data Injection (4P)", bullet_points=["Generated from direct dictionary input"]),
        SlideContent(title="DB Data Fetching (SWOT)", bullet_points=["Generated from database record"])
    ]
    schema = PresentationSchema(topic="Hybrid Strategy Report", slides=slides)
    
    # 3. Define Design Schema with Hybrid Data Sources
    design_schema = [
        # Slide 1: Direct Data (4P)
        {
            "diagram_type": "4p",
            "data_source": {
                "type": "direct",
                "content": {
                    "product": ["Premium Quality", "Innovative Design"],
                    "price": ["High End", "Skimming Strategy"],
                    "place": ["Global Retail", "Online Store"],
                    "promotion": ["Social Media", "Influencer Marketing"]
                }
            }
        },
        # Slide 2: DB Data (SWOT)
        {
            "diagram_type": "swot",
            "data_source": {
                "type": "db",
                "institution_id": inst_id
            }
        }
    ]
    
    # 4. Generate Presentation
    service = PPTXService(output_dir="output/tests")
    output_file = service.create_presentation(schema, filename="hybrid_strategy_test.pptx", design_schema=design_schema)
    
    print(f"Presentation generated at: {output_file}")
    
    # Cleanup
    db.delete(analysis)
    db.delete(inst)
    db.commit()
    db.close()
    
    return output_file

if __name__ == "__main__":
    test_hybrid_strategy_integration()
