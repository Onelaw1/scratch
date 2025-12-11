import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from src.models.schema import PresentationSchema, SlideContent

load_dotenv()

from src.services.memory_service import MemoryService
from src.agents.critic import CriticAgent

class PlannerAgent:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.memory = MemoryService()
        self.critic = CriticAgent(model_name)

    def plan_presentation(self, topic: str) -> PresentationSchema:
        print(f"Planner Agent: Creating outline for '{topic}'...")
        
        # 1. Retrieve Context from Memory
        context = self.memory.retrieve_context(topic)
        print(f"  [Memory] Retrieved Context: {context[:100]}...")

        # 2. Initial Planning Loop (with Critique)
        max_retries = 2
        current_plan_json = None
        
        for attempt in range(max_retries + 1):
            # Generate Plan
            prompt = self._build_prompt(topic, context, feedback=None if attempt == 0 else critique.feedback)
            current_plan_json = self._generate_and_parse(prompt)
            
            # 3. Critique
            critique = self.critic.critique_plan(topic, current_plan_json, context)
            print(f"  [Critic] Score: {critique.score}, Approved: {critique.is_approved}")
            
            if critique.is_approved:
                break
            
            print(f"  [Planner] Revising based on feedback: {critique.feedback[:100]}...")

        return PresentationSchema(**current_plan_json)

    def _build_prompt(self, topic: str, context: str, feedback: Optional[str] = None) -> str:
        base_prompt = f"""
        You are a Senior Engagement Manager at a top-tier strategy consulting firm (e.g., McKinsey, BCG, Bain).
        Your goal is to create a compelling, logic-driven presentation outline on: "{topic}".
        
        ### CONTEXT & PERSONA (MUST ADHERE):
        {context}
        
        ### CRITICAL INSTRUCTIONS:
        1. **SCQA Framework**: Structure the narrative using Situation, Complication, Question, and Answer.
        2. **MECE Principle**: Ensure all slide groups and bullet points are Mutually Exclusive and Collectively Exhaustive.
        3. **Action Titles**: Every slide title must be a full sentence that conveys the main insight (the "So What?"), not just a generic label like "Introduction".
        4. **Pyramid Principle**: Start with the main conclusion, then support it with arguments.

        ### PROCESS:
        Before generating the JSON, you MUST output a <thinking> block where you:
        - Define the Core Question.
        - Draft the SCQA.
        - Verify MECE structure of your proposed sections.
        """
        
        if feedback:
            base_prompt += f"\n\n### CRITICAL FEEDBACK (FIX THIS): \n{feedback}\n"

        base_prompt += """
        After your thinking, output the result strictly as a valid JSON object matching this structure:
        {
            "topic": "The main topic",
            "slides": [
                {
                    "title": "Action Title (Full Sentence)",
                    "bullet_points": ["Point 1", "Point 2", "Point 3"],
                    "image_description": "Description of a relevant image",
                    "speaker_notes": "Notes for the speaker"
                }
            ]
        }
        
        Create at least 5 slides including Introduction and Conclusion.
        """
        return base_prompt

    def _generate_and_parse(self, prompt: str) -> dict:
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Robust JSON extraction to handle <thinking> blocks
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Fallback: find the first outer brace pair
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = text[start:end]
                else:
                    json_str = text

            return json.loads(json_str)
            
        except Exception as e:
            print(f"Planner Agent Error: {e}")
            # Return a basic error structure to avoid crashing
            return {
                "topic": "Error",
                "slides": [{"title": "Error", "bullet_points": [str(e)], "image_description": "", "speaker_notes": ""}]
            }
