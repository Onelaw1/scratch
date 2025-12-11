from src.services.visual_engine import VisualEngine
from typing import Dict, List, Optional
import os

class ChartService:
    def __init__(self, output_dir: str = "output/charts"):
        self.output_dir = output_dir
        self.engine = VisualEngine(output_dir)

    def generate_bar_chart(self, data: Dict[str, float], title: str, filename: str) -> str:
        """Generate a bar chart using VisualEngine."""
        return self.engine.generate_bar_chart(data, title, filename)

    def generate_line_chart(self, data: Dict[str, List[float]], title: str, filename: str) -> str:
        """Generate a line chart using VisualEngine."""
        # Infer x_labels from the length of the first data series
        if not data:
            return ""
        
        first_series = next(iter(data.values()))
        x_labels = [str(i) for i in range(1, len(first_series) + 1)]
        
        return self.engine.generate_line_chart(data, x_labels, title, filename)

    def generate_pie_chart(self, data: Dict[str, float], title: str, filename: str) -> str:
        """Generate a pie/donut chart using VisualEngine."""
        return self.engine.generate_donut_chart(data, title, filename)

    # --- Advanced Charts ---

    def generate_waterfall(self, categories: List[str], values: List[float], title: str, filename: str) -> str:
        return self.engine.generate_waterfall(categories, values, title, filename)

    def generate_sankey(self, labels: List[str], source: List[int], target: List[int], values: List[float], title: str, filename: str) -> str:
        return self.engine.generate_sankey(labels, source, target, values, title, filename)

    def generate_heatmap(self, data: List[List[float]], x_labels: List[str], y_labels: List[str], title: str, filename: str) -> str:
        return self.engine.generate_heatmap(data, x_labels, y_labels, title, filename)

    def generate_treemap(self, labels: List[str], parents: List[str], values: List[float], title: str, filename: str) -> str:
        return self.engine.generate_treemap(labels, parents, values, title, filename)

    def generate_radar(self, categories: List[str], data: Dict[str, List[float]], title: str, filename: str) -> str:
        return self.engine.generate_radar(categories, data, title, filename)
