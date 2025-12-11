from typing import Dict, Any, Optional
import json
import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class DataIngestionService:
    """
    Service to ingest and normalize data from various sources (JSON, Dict, Excel, Image)
    for strategic analysis frameworks.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            print("Warning: GOOGLE_API_KEY not found. Image ingestion will not work.")
            self.model = None
    
    def ingest_data(self, data: Any, source_type: str = "dict") -> Dict[str, Any]:
        """
        Ingest data from a source and return a normalized dictionary.
        
        Args:
            data: The input data (dict, json string, file path, bytes, etc.)
            source_type: Type of source ("dict", "json", "excel", "image")
            
        Returns:
            Normalized dictionary ready for DiagramService
        """
        if source_type == "dict":
            return self._ingest_dict(data)
        elif source_type == "json":
            return self._ingest_json(data)
        elif source_type == "excel":
            return self._ingest_excel(data)
        elif source_type == "image":
            return self._ingest_image(data)
        else:
            print(f"Warning: Unsupported source type '{source_type}'. Returning empty dict.")
            return {}

    def _ingest_dict(self, data: Dict) -> Dict:
        if not isinstance(data, dict):
            print("Error: Data is not a dictionary.")
            return {}
        return data

    def _ingest_json(self, data: str) -> Dict:
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}

    def _ingest_excel(self, file_path_or_buffer: Any) -> Dict:
        """
        Ingest data from Excel.
        Expected format: Two columns, "Category" and "Item".
        Example:
            Category | Item
            Strengths| Strong Brand
            Strengths| Global Presence
            Weaknesses| High Cost
        """
        try:
            df = pd.read_excel(file_path_or_buffer)
            
            # Normalize column names
            df.columns = [str(col).lower().strip() for col in df.columns]
            
            if "category" not in df.columns or "item" not in df.columns:
                print("Error: Excel must have 'Category' and 'Item' columns.")
                return {}
            
            result = {}
            for _, row in df.iterrows():
                category = str(row["category"]).strip()
                item = str(row["item"]).strip()
                
                if category not in result:
                    result[category] = []
                result[category].append(item)
            
            return result
        except Exception as e:
            print(f"Error reading Excel: {e}")
            return {}

    def _ingest_image(self, image_path_or_bytes: Any) -> Dict:
        """
        Ingest data from Image using Gemini Vision.
        """
        if not self.model:
            print("Error: Gemini model not initialized.")
            return {}
            
        try:
            # Prepare image data
            if isinstance(image_path_or_bytes, str) and os.path.exists(image_path_or_bytes):
                import PIL.Image
                image = PIL.Image.open(image_path_or_bytes)
            else:
                # Assume bytes or other format supported by Gemini
                # For simplicity in this phase, let's assume file path or PIL image
                # If bytes, we might need to convert. 
                # Let's stick to file path for now as primary use case in CLI/Test.
                print("Error: Currently only file paths are supported for image ingestion.")
                return {}

            prompt = """
            Analyze this image of a business framework (e.g., SWOT, 4P, BCG, etc.).
            Extract the text content into a structured JSON format.
            
            If it's a SWOT analysis, return:
            {
                "Strengths": ["item1", ...],
                "Weaknesses": ["item1", ...],
                "Opportunities": ["item1", ...],
                "Threats": ["item1", ...]
            }
            
            If it's 4P, return:
            {
                "Product": [...],
                "Price": [...],
                "Place": [...],
                "Promotion": [...]
            }
            
            For other diagrams, use appropriate category keys.
            Return ONLY valid JSON.
            """
            
            response = self.model.generate_content([prompt, image])
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
                
            return json.loads(text)
            
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return {}
