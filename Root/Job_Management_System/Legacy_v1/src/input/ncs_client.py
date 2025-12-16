import requests
import os
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class NCSClient:
    BASE_URL = "https://api.odcloud.kr/api/15083321/v1/uddi:d6120556-7544-44ee-ac57-8fa979a60247"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NCS_API_KEY")
        if not self.api_key:
            print("Warning: NCS_API_KEY not found in environment variables.")

    def search_ncs(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Fetches NCS data from the API.
        """
        params = {
            "page": page,
            "perPage": per_page,
            "serviceKey": self.api_key
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, headers={"accept": "*/*"})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching NCS data: {e}")
            return {}

    def get_dummy_data(self) -> List[Dict[str, Any]]:
        """
        Returns dummy data for testing if API is unavailable.
        """
        return [
            {
                "ncs_code": "01010101",
                "unit_name": "Business Strategy Planning",
                "unit_definition": "Establishing mid-to-long term business strategies."
            },
            {
                "ncs_code": "20010202",
                "unit_name": "SW Architecture Design",
                "unit_definition": "Designing the structure of software systems."
            }
        ]
