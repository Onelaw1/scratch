import os
import sys


# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.pptx_service import PPTXService
from src.services.job_data_extractor import JobDataExtractor
from src.models.schema import PresentationSchema, SlideContent

def test_real_data_integration():
    print("Testing integration with real Job Management System data...")
    
    # Initialize services
    extractor = JobDataExtractor()
    service = PPTXService(output_dir="output/tests")
    
    try:
        # 1. Extract Data
        print("Extracting data...")
        org_data = extractor.get_org_hierarchy()
        fte_data = extractor.get_fte_by_department()
        raci_data = extractor.get_job_tasks_matrix()
        
        print(f"Org Data Keys: {list(org_data.keys())}")
        print(f"FTE Data Keys: {list(fte_data.keys())}")
        print(f"RACI Data Keys: {list(raci_data.keys())}")
        
        # 2. Create Schema
        schema = PresentationSchema(
            topic="Real Data Integration Test",
            slides=[
                SlideContent(
                    title="Organizational Structure", 
                    bullet_points=["Current organizational hierarchy based on database records."]
                ),
                SlideContent(
                    title="Workforce Planning (FTE)", 
                    bullet_points=["Comparison of current vs required FTE by department."]
                ),
                SlideContent(
                    title="RACI Matrix", 
                    bullet_points=["Roles and responsibilities for key job tasks."]
                )
            ]
        )
        
        # 3. Create Design Schema with Real Data
        design_schema = [
            {
                "layout_index": 1, 
                "diagram_type": "org_chart", 
                "diagram_data": org_data
            },
            {
                "layout_index": 1, 
                "diagram_type": "fte_model", 
                "diagram_data": fte_data
            },
            {
                "layout_index": 1, 
                "diagram_type": "raci", 
                "diagram_data": raci_data
            }
        ]
        
        # 4. Generate Presentation
        output_path = service.create_presentation(
            schema, 
            filename="real_data_test.pptx", 
            design_schema=design_schema
        )
        
        print(f"Presentation created at: {output_path}")
        
        # 5. Verify
        if os.path.exists(output_path):
            print("SUCCESS: Presentation file created successfully.")
        else:
            print("FAILURE: Presentation file was not created.")
            
    except Exception as e:
        print(f"ERROR: Integration test failed with exception: {e}")
        import traceback
        traceback.print_exc()
    finally:
        extractor.close()

if __name__ == "__main__":
    test_real_data_integration()
