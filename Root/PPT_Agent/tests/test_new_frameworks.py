import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.services.pptx_service import PPTXService
from src.models.schema import PresentationSchema, SlideContent

def test_new_frameworks():
    print("Testing new frameworks...")
    service = PPTXService(output_dir="output/tests")
    
    # Futures Wheel Data
    futures_wheel_data = {
        "event": "AI Adoption",
        "consequences": [
            "Job Displacement",
            "Productivity Boost",
            "New Skill Requirements",
            "Ethical Concerns",
            "Data Privacy Issues",
            "Market Disruption"
        ]
    }
    
    # Kano Model Data
    kano_data = {
        "Basic": ["Login", "Security", "Reliability"],
        "Performance": ["Speed", "Storage Capacity", "Battery Life"],
        "Delighters": ["AI Assistant", "Personalization", "Voice Control"]
    }
    
    schema = PresentationSchema(
        topic="New Frameworks Test",
        slides=[
            SlideContent(
                title="Futures Wheel: AI Adoption",
                bullet_points=["Analyzing the impact of AI adoption."]
            ),
            SlideContent(
                title="Kano Model: Product Features",
                bullet_points=["Prioritizing features based on customer satisfaction."]
            )
        ]
    )
    
    # 3C Analysis Data
    three_c_data = {
        "Customer": ["Gen Z", "Tech Savvy"],
        "Company": ["Innovation", "Agile"],
        "Competitor": ["Legacy", "Slow"]
    }

    # Impact/Effort Matrix Data
    impact_effort_data = {
        "Quick Wins": ["Feature A", "Bug Fix B"],
        "Major Projects": ["Platform Re-architecture"],
        "Fill-ins": ["Icon Update"],
        "Thankless Tasks": ["Manual Data Entry"]
    }

    # RACI Matrix Data
    raci_data = {
        "Task 1": {"PM": "R", "Dev": "C", "QA": "I", "Ops": "I"},
        "Task 2": {"PM": "A", "Dev": "R", "QA": "C", "Ops": "I"},
        "Task 3": {"PM": "I", "Dev": "R", "QA": "R", "Ops": "C"}
    }

    # Gantt Chart Data
    gantt_data = {
        "Phase 1": {"start": 0.0, "duration": 0.2},
        "Phase 2": {"start": 0.2, "duration": 0.3},
        "Phase 3": {"start": 0.5, "duration": 0.4}
    }

    # Org Chart Data
    org_data = {
        "CEO": "John Doe",
        "C-Level": ["Jane Smith (CTO)", "Bob Jones (CFO)", "Alice Brown (CMO)"]
    }

    # Fishbone Diagram Data
    fishbone_data = {
        "Problem": "High Churn",
        "Man": ["Lack of Training", "Low Morale"],
        "Machine": ["Legacy System", "Slow Network"],
        "Method": ["Poor Onboarding", "Complex Process"],
        "Material": ["Outdated Docs"],
        "Measurement": ["Wrong KPIs"],
        "Environment": ["Remote Work"]
    }

    # Value Chain Data
    value_chain_data = {
        "Inbound": ["Raw Materials"],
        "Operations": ["Manufacturing"],
        "Outbound": ["Distribution"],
        "Marketing": ["Sales"],
        "Service": ["Support"]
    }

    # Business Model Canvas Data
    bmc_data = {
        "Key Partners": ["Suppliers"],
        "Key Activities": ["Production"],
        "Value Propositions": ["Quality"],
        "Customer Relationships": ["Personal"],
        "Customer Segments": ["Mass Market"],
        "Key Resources": ["Factory"],
        "Channels": ["Retail"],
        "Cost Structure": ["Fixed Costs"],
        "Revenue Streams": ["Sales"]
    }

    # McKinsey 7S Data
    mckinsey_data = {}

    # Decision Tree Data
    decision_tree_data = {
        "root": "Launch?",
        "options": ["Yes", "No"]
    }

    # Lean Canvas Data
    lean_canvas_data = {
        "Problem": ["Inefficiency"],
        "Solution": ["Automation"],
        "Unique Value Proposition": ["Speed"],
        "Unfair Advantage": ["IP"],
        "Customer Segments": ["Startups"],
        "Key Metrics": ["DAU"],
        "Channels": ["Web"],
        "Cost Structure": ["Hosting"],
        "Revenue Streams": ["Subscription"]
    }

    # 9-Box Grid Data
    nine_box_data = {
        "Stars": ["Alice"],
        "Core Players": ["Bob"],
        "Low Performers": ["Charlie"]
    }

    # FTE Model Data
    fte_data = {
        "Dept A": {"current": 5, "required": 7},
        "Dept B": {"current": 10, "required": 8}
    }

    # AHP Data
    ahp_data = {
        "goal": "Select Vendor",
        "criteria": {"Cost": 0.4, "Quality": 0.6},
        "alternatives": {"Vendor A": 0.7, "Vendor B": 0.3}
    }

    # OCAI Data
    ocai_data = {
        "Clan": 0.3,
        "Adhocracy": 0.4,
        "Market": 0.2,
        "Hierarchy": 0.1
    }

    schema = PresentationSchema(
        topic="Advanced Frameworks Test",
        slides=[
            SlideContent(title="Fishbone Diagram", bullet_points=["Root Cause Analysis"]),
            SlideContent(title="Value Chain", bullet_points=["Porter's Value Chain"]),
            SlideContent(title="Business Model Canvas", bullet_points=["Business Model"]),
            SlideContent(title="McKinsey 7S", bullet_points=["Organizational Alignment"]),
            SlideContent(title="Decision Tree", bullet_points=["Decision Making"]),
            SlideContent(title="Lean Canvas", bullet_points=["Lean Startup"]),
            SlideContent(title="9-Box Grid", bullet_points=["Talent Management"]),
            SlideContent(title="FTE Model", bullet_points=["Workforce Planning"]),
            SlideContent(title="AHP", bullet_points=["Decision Hierarchy"]),
            SlideContent(title="OCAI", bullet_points=["Culture Assessment"])
        ]
    )
    
    design_schema = [
        {"layout_index": 1, "diagram_type": "fishbone", "diagram_data": fishbone_data},
        {"layout_index": 1, "diagram_type": "value_chain", "diagram_data": value_chain_data},
        {"layout_index": 1, "diagram_type": "bmc", "diagram_data": bmc_data},
        {"layout_index": 1, "diagram_type": "mckinsey_7s", "diagram_data": mckinsey_data},
        {"layout_index": 1, "diagram_type": "decision_tree", "diagram_data": decision_tree_data},
        {"layout_index": 1, "diagram_type": "lean_canvas", "diagram_data": lean_canvas_data},
        {"layout_index": 1, "diagram_type": "nine_box", "diagram_data": nine_box_data},
        {"layout_index": 1, "diagram_type": "fte_model", "diagram_data": fte_data},
        {"layout_index": 1, "diagram_type": "ahp", "diagram_data": ahp_data},
        {"layout_index": 1, "diagram_type": "ocai", "diagram_data": ocai_data}
    ]
    
    output_path = service.create_presentation(schema, filename="test_new_frameworks.pptx", design_schema=design_schema)
    print(f"Presentation created at: {output_path}")
    
    if os.path.exists(output_path):
        print("SUCCESS: File exists.")
    else:
        print("FAILURE: File not created.")

if __name__ == "__main__":
    test_new_frameworks()
