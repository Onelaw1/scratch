import os
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

class CritiqueResult(BaseModel):
    score: int = Field(..., description="Score from 0 to 100")
    feedback: str = Field(..., description="Detailed critique of the plan")
    is_approved: bool = Field(..., description="Whether the plan meets the standards")
    suggestions: List[str] = Field(..., description="Specific actionable suggestions for improvement")

class CriticAgent:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def critique_plan(self, topic: str, plan_json: dict, context: str = "") -> CritiqueResult:
        print(f"Critic Agent: Reviewing plan for '{topic}'...")
        
        prompt = f"""
        You are a **Ruthless Academic Critic** (Professor/Evaluation Committee Member).
        Your goal is to evaluate this plan as if it were a submission for a **Public Institution Management Evaluation**.

        **Context from Memory**:
        {context}

        **The Plan to Review**:
        Topic: {topic}
        Content: {plan_json}

        **Critique Criteria (The Evaluator's Eye)**:
        1. **Evidence (증거주의)**: Is every claim backed by data or a manual reference?
        2. **Logic (논리적 정합성)**: Is the flow academically rigorous? (Thesis -> Evidence -> Conclusion)
        3. **Compliance (규정 준수)**: Does it explicitly mention the "Management Evaluation Manual" indicators?
        4. **Public Value (공익성)**: Is the social contribution tangible and measurable?

        **Output Format**:
        Return a valid JSON object matching this structure:
        {{
            "score": 75,
            "feedback": "Logic is sound, but lacks specific references to the Evaluation Manual...",
            "is_approved": false,
            "suggestions": ["Cite specific Evaluation Indicator (e.g., 'Leadership')", "Add quantitative evidence for Social Value"]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Robust JSON extraction
            import re
            import json
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                start = text.find('{')
                end = text.rfind('}') + 1
                json_str = text[start:end] if start != -1 else text

            data = json.loads(json_str)
            return CritiqueResult(**data)
            
        except Exception as e:
            print(f"Critic Agent Error: {e}")
            return CritiqueResult(
                score=0,
                feedback=f"Error during critique: {str(e)}",
                is_approved=False,
                suggestions=["System Error - Please Retry"]
            )
