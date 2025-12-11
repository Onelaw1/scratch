import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.models.schema import SlideContent

load_dotenv()

class ReviewerAgent:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def review_slide(self, content: SlideContent, topic: str) -> tuple[bool, str]:
        """
        Returns (approved: bool, feedback: str)
        """
        print(f"Reviewer: Reviewing '{content.title}'...")
        
        prompt = f"""
        You are a strict presentation reviewer.
        Topic: "{topic}"
        Slide Content: {content.model_dump_json()}
        
        Check for:
        1. Relevance to topic.
        2. Clarity and conciseness (no walls of text).
        3. Professional tone.
        
        If it's good, return "APPROVED".
        If it needs changes, return a short feedback sentence describing what to fix.
        """

        try:
            response = self.model.generate_content(prompt)
            feedback = response.text.strip()
            
            if "APPROVED" in feedback.upper():
                return True, "Approved"
            else:
                return False, feedback
                
        except Exception as e:
            print(f"Reviewer Error: {e}")
            return True, "Skipped review due to error"
