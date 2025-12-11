import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from src.models.schema import SlideContent

load_dotenv()

class ContentWriterAgent:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def write_slide_content(self, topic: str, slide_title: str, slide_intent: str) -> SlideContent:
        print(f"Content Writer: Writing content for slide '{slide_title}'...")
        
        prompt = f"""
        You are an expert presentation content writer.
        Topic: "{topic}"
        Slide Title: "{slide_title}"
        Slide Intent/Context: "{slide_intent}"
        
        Generate detailed content for this slide.
        Return strictly valid JSON matching this structure:
        {{
            "title": "{slide_title}",
            "bullet_points": ["Detailed point 1", "Detailed point 2", "Detailed point 3"],
            "image_description": "A detailed prompt for an AI image generator to create a relevant visual.",
            "speaker_notes": "Comprehensive speaker notes explaining these points."
        }}
        
        Make the bullet points concise but impactful.
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
                
            data = json.loads(text)
            return SlideContent(**data)
            
        except Exception as e:
            print(f"Content Writer Error: {e}")
            return SlideContent(
                title=slide_title,
                bullet_points=["Error generating content."],
                speaker_notes=f"Error: {str(e)}"
            )
