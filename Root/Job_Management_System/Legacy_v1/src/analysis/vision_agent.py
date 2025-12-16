import os
import json
import google.generativeai as genai
from PIL import Image
from typing import Optional, Tuple, Dict, Any
from .schema import JangpyoSlide
from .prompts import PromptEngine
from dotenv import load_dotenv

load_dotenv()

class VisionAgent:
    """
    The 'Brain' of the system. Uses Gemini Vision to analyze slides.
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API Key is required. Set GOOGLE_API_KEY env var or pass it to constructor.")
            
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.prompt_engine = PromptEngine()

    def analyze_slide(self, image: Image.Image, slide_number: int = 1) -> Tuple[JangpyoSlide, Dict[str, Any]]:
        """
        Analyzes a single slide image and returns structured data and usage metrics.
        Returns: (JangpyoSlide object, usage_dict)
        """
        system_prompt = self.prompt_engine.get_system_prompt()
        
        # Combine system prompt with specific request
        full_prompt = [
            system_prompt,
            f"Analyze this slide image (Slide #{slide_number}). Return ONLY the JSON.",
            image
        ]
        
        print(f"Sending Slide #{slide_number} to Vision AI...")
        response = self.model.generate_content(full_prompt)
        
        # Extract usage metadata
        usage = {}
        if hasattr(response, 'usage_metadata'):
            usage = {
                "prompt_token_count": response.usage_metadata.prompt_token_count,
                "candidates_token_count": response.usage_metadata.candidates_token_count,
                "total_token_count": response.usage_metadata.total_token_count
            }
        
        try:
            # Clean up response (remove markdown code blocks if present)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            data = json.loads(text)
            data["slide_number"] = slide_number # Ensure slide number is correct
            
            return JangpyoSlide(**data), usage
            
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON from AI response.")
            print("Raw Response:", response.text)
            raise
        except Exception as e:
            print(f"Error validating schema: {e}")
            raise

if __name__ == "__main__":
    # Test stub
    # agent = VisionAgent()
    # result, usage = agent.analyze_slide(Image.open("test.png"))
    # print(result, usage)
    pass
