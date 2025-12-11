import os
from openai import OpenAI
from dotenv import load_dotenv
import requests
from typing import Optional

load_dotenv()

class ImageService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        # If no OpenAI key, we might need a fallback or just return None
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
            print("Warning: OPENAI_API_KEY not found. Image generation will be disabled.")

    def generate_image(self, prompt: str, output_path: str) -> Optional[str]:
        if not self.client:
            return None
            
        print(f"ImageService: Generating image for prompt: '{prompt[:50]}...'")
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download the image
            img_data = requests.get(image_url).content
            with open(output_path, 'wb') as handler:
                handler.write(img_data)
                
            return output_path
            
        except Exception as e:
            print(f"ImageService Error: {e}")
            return None
