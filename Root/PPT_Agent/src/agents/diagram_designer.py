import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Optional, Dict

load_dotenv()

class DiagramDesignerAgent:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def analyze_for_diagram(self, slide_title: str, bullet_points: list, topic: str) -> Optional[Dict]:
        """
        Determines if a slide needs a business framework diagram.
        Returns diagram specification or None.
        """
        print(f"Diagram Designer: Analyzing '{slide_title}' for framework diagrams...")
        
        prompt = f"""
        You are a business consulting expert.
        Topic: "{topic}"
        Slide Title: "{slide_title}"
        Content: {bullet_points}
        
        Determine if this slide would benefit from a business framework diagram.
        
        If YES, return JSON with:
        {{
            "needs_diagram": true,
            "diagram_type": "swot" | "workflow" | "4p" | "bcg" | "eisenhower" | "porters" | "ge_matrix" | "scenario" | "value_chain" | "bmc" | "mckinsey_7s" | "ansoff" | "stakeholder" | "3c" | "impact_effort" | "gantt" | "fishbone" | "org_chart" | "raci" | "decision_tree" | "lean_canvas" | "nine_box" | "fte_model" | "ahp" | "ocai",
            "data": {{
                // For SWOT:
                "Strengths": ["item1", "item2"],
                "Weaknesses": ["item1", "item2"],
                "Opportunities": ["item1", "item2"],
                "Threats": ["item1", "item2"]
                
                // For Workflow:
                "steps": ["Step 1", "Step 2", "Step 3"]
                
                // For 4P:
                "Product": ["feature1", "feature2"],
                "Price": ["strategy1", "strategy2"],
                "Place": ["channel1", "channel2"],
                "Promotion": ["tactic1", "tactic2"]
                
                // For BCG Matrix:
                "Stars": ["product1"],
                "Cash Cows": ["product2"],
                "Question Marks": ["product3"],
                "Dogs": ["product4"]
                
                // For Eisenhower Matrix:
                "Do First": ["task1"],
                "Schedule": ["task2"],
                "Delegate": ["task3"],
                "Eliminate": ["task4"]
                
                // For Porter's 5 Forces:
                "New Entrants": "threat level",
                "Suppliers": "power level",
                "Buyers": "power level",
                "Substitutes": "threat level"
                
                // For GE Matrix (3x3):
                "High/High": ["product1"],
                "Med/High": ["product2"],
                ... (9 cells total)
                
                // For Scenario Planning:
                "Scenario 1": {{"name": "Best Case", "description": "...", "factors": ["factor1"]}},
                "Scenario 2": {{"name": "Worst Case", "description": "...", "factors": ["factor1"]}},
                "Scenario 3": {{"name": "Status Quo", "description": "...", "factors": ["factor1"]}},
                "Scenario 4": {{"name": "Disruptive", "description": "...", "factors": ["factor1"]}}
                
                // For Value Chain:
                "Inbound": ["activity1"],
                "Operations": ["activity1"],
                "Outbound": ["activity1"],
                "Marketing": ["activity1"],
                "Service": ["activity1"],
                "Infrastructure": ["activity1"],
                "HR Management": ["activity1"],
                "Technology": ["activity1"],
                "Procurement": ["activity1"]
            }}
        }}
        
        If NO, return: {{"needs_diagram": false}}
        
        Use SWOT for: strengths/weaknesses analysis, competitive analysis
        Use Workflow for: processes, steps, procedures, timelines
        Use 4P for: marketing strategy, product launch
        Use BCG for: product portfolio analysis, market position
        Use Eisenhower for: task prioritization, time management
        Use Porters for: industry analysis, competitive forces
        Use GE Matrix for: multi-dimensional portfolio analysis, business unit evaluation
        Use Scenario for: future planning, strategic scenarios, uncertainty analysis
        Use Value Chain for: operational analysis, value creation process
        Use BMC for: business model design, startup planning
        Use McKinsey 7S for: organizational alignment, change management
        Use Ansoff for: growth strategy, market expansion
        Use Stakeholder for: stakeholder analysis, engagement planning
        Use 3C for: strategic analysis, competitive positioning
        Use Impact/Effort for: project prioritization, resource allocation
        Use Gantt for: project timeline, task scheduling
        Use Fishbone for: root cause analysis, quality management
        Use Org Chart for: organizational structure, hierarchy
        Use RACI for: responsibility assignment, governance
        Use Decision Tree for: decision analysis, risk assessment
        Use Lean Canvas for: lean startup, business model validation
        Use 9-Box Grid for: talent assessment, succession planning
        Use FTE Model for: workforce planning, headcount optimization
        Use AHP for: decision making, prioritization with multiple criteria
        Use OCAI for: organizational culture assessment, culture change
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
                
            data = json.loads(text)
            
            if not data.get("needs_diagram", False):
                return None
                
            return {
                "diagram_type": data.get("diagram_type"),
                "data": data.get("data", {})
            }
            
        except Exception as e:
            print(f"Diagram Designer Error: {e}")
            return None
