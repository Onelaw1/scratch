from src.models.schema import PresentationSchema, SlideContent
from src.services.pptx_service import PPTXService
from src.services.image_service import ImageService
from src.agents.planner import PlannerAgent
from src.agents.content_writer import ContentWriterAgent
from src.agents.designer import DesignerAgent
from src.agents.reviewer import ReviewerAgent
from src.agents.data_analyst import DataAnalystAgent
from src.agents.diagram_designer import DiagramDesignerAgent
from typing import Optional
import os

class Orchestrator:
    def __init__(self):
        self.pptx_service = PPTXService()
        self.image_service = ImageService()
        self.planner = PlannerAgent()
        self.content_writer = ContentWriterAgent()
        self.designer = DesignerAgent()
        self.reviewer = ReviewerAgent()
        self.data_analyst = DataAnalystAgent()
        self.diagram_designer = DiagramDesignerAgent()

    def generate_presentation(self, topic: str, filename: Optional[str] = None) -> str:
        # 1. Plan
        print("--- Phase 1: Planning ---")
        schema = self.planner.plan_presentation(topic)
        
        # 2. Generate Content & Design (Iterative Loop)
        print("--- Phase 2: Content Generation, Design & Review ---")
        final_slides = []
        design_schemas = []
        
        for i, slide_outline in enumerate(schema.slides):
            print(f"\nProcessing Slide {i+1}: {slide_outline.title}")
            
            # Draft
            context = "; ".join(slide_outline.bullet_points)
            draft_content = self.content_writer.write_slide_content(topic, slide_outline.title, context)
            
            # Review
            approved, feedback = self.reviewer.review_slide(draft_content, topic)
            if not approved:
                print(f"  Reviewer Feedback: {feedback}")
                print("  Refining content...")
                refined_context = f"{context}. Feedback to address: {feedback}"
                draft_content = self.content_writer.write_slide_content(topic, slide_outline.title, refined_context)
                print("  Content refined.")
            
            # Design
            style = self.designer.design_slide(draft_content)
            
            # Diagram Analysis (Frameworks like SWOT, Workflow)
            diagram_info = self.diagram_designer.analyze_for_diagram(
                draft_content.title,
                draft_content.bullet_points,
                topic
            )
            if diagram_info:
                style["diagram_type"] = diagram_info["diagram_type"]
                style["diagram_data"] = diagram_info["data"]
                print(f"  Diagram detected: {diagram_info['diagram_type']}")
            
            # Data Analysis (Charts) - only if no diagram
            chart_info = None
            if not diagram_info:
                chart_info = self.data_analyst.analyze_slide_for_charts(
                    draft_content.title, 
                    draft_content.bullet_points, 
                    topic
                )
                if chart_info:
                    style["chart_path"] = chart_info["chart_path"]
                    print(f"  Chart generated: {chart_info['chart_type']}")
            
            # Image Generation (if applicable and no chart)
            if draft_content.image_description and not chart_info:
                print("  Generating Image...")
                image_filename = f"slide_{i+1}.png"
                image_path = os.path.join("output", "images", image_filename)
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                
                generated_path = self.image_service.generate_image(draft_content.image_description, image_path)
                if generated_path:
                    style["image_path"] = generated_path
                    print(f"  Image saved to {generated_path}")
            
            final_slides.append(draft_content)
            design_schemas.append(style)
            
        # Update schema
        schema.slides = final_slides
        
        # 3. Generate PPTX
        print("--- Phase 3: Final Generation ---")
        if filename is None:
            filename = f"{topic.replace(' ', '_').lower()}.pptx"
        
        output_path = self.pptx_service.create_presentation(schema, filename, design_schema=design_schemas)
        print(f"Presentation generated at: {output_path}")
        return output_path
