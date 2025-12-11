import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from src.services.chart_service import ChartService
from typing import Optional, Dict

load_dotenv()

class DataAnalystAgent:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.chart_service = ChartService()

    def analyze_slide_for_charts(self, slide_title: str, bullet_points: list, topic: str) -> Optional[Dict]:
        """
        Determines if a slide would benefit from a chart and generates it.
        Returns chart info or None.
        """
        print(f"Data Analyst: Analyzing '{slide_title}' for chart opportunities...")
        
        prompt = f"""
        You are a data visualization expert.
        Topic: "{topic}"
        Slide Title: "{slide_title}"
        Content: {bullet_points}
        
        Determine if this slide would benefit from a chart/graph.
        If YES, return JSON with:
        {{
            "needs_chart": true,
            "chart_type": "bar" | "line" | "pie",
            "chart_title": "Title for the chart",
            "data": {{"Label1": value1, "Label2": value2, ...}}
        }}
        
        If NO, return: {{"needs_chart": false}}
        
        Only suggest charts for slides with quantitative data or comparisons.
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
                
            data = json.loads(text)
            
            if not data.get("needs_chart", False):
                return None
                
            # Generate the chart
            chart_type = data.get("chart_type", "bar")
            chart_title = data.get("chart_title", slide_title)
            chart_data = data.get("data", {})
            
            filename = f"{slide_title.replace(' ', '_').lower()}_chart.png"
            
            if chart_type == "bar":
                path = self.chart_service.generate_bar_chart(chart_data, chart_title, filename)
            elif chart_type == "line":
                path = self.chart_service.generate_line_chart(chart_data, chart_title, filename)
            elif chart_type == "pie":
                path = self.chart_service.generate_pie_chart(chart_data, chart_title, filename)
            else:
                return None
                
            return {
                "chart_path": path,
                "chart_type": chart_type,
                "chart_title": chart_title
            }
            
        except Exception as e:
            print(f"Data Analyst Error: {e}")
            return None
