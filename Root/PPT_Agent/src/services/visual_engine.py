import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
import os
from typing import Dict, List, Optional, Union, Any

class VisualEngine:
    """
    Advanced Visual Engine for generating consulting-grade charts using Plotly.
    Focuses on McKinsey/BCG style aesthetics: clean, minimal, impactful.
    """
    
    def __init__(self, output_dir: str = "output/charts"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Define Consulting Color Palette
        self.colors = {
            "primary": "#002060",      # Navy Blue (McKinsey-ish)
            "secondary": "#00A9E0",    # Bright Blue
            "accent": "#7F7F7F",       # Grey
            "highlight": "#E4002B",    # Red for alerts/negatives
            "positive": "#009B77",     # Green
            "background": "#FFFFFF",
            "text": "#333333",
            "grid": "#E5E5E5"
        }
        
        # Set default template
        self._setup_theme()

    def _setup_theme(self):
        """Configure global Plotly theme settings for professional look."""
        pio.templates["consulting"] = go.layout.Template(
            layout=go.Layout(
                font=dict(family="Arial, sans-serif", color=self.colors["text"], size=14),
                title=dict(font=dict(size=20, color=self.colors["primary"], family="Arial, sans-serif")),
                plot_bgcolor=self.colors["background"],
                paper_bgcolor=self.colors["background"],
                xaxis=dict(
                    showgrid=False, 
                    zeroline=True, 
                    zerolinecolor=self.colors["grid"],
                    linecolor=self.colors["accent"],
                    tickfont=dict(size=12)
                ),
                yaxis=dict(
                    showgrid=True, 
                    gridcolor=self.colors["grid"], 
                    zeroline=False,
                    tickfont=dict(size=12)
                ),
                colorway=[
                    self.colors["primary"], 
                    self.colors["secondary"], 
                    "#767171", # Dark Grey
                    "#007CC3", # Medium Blue
                    "#FFC000", # Yellow/Gold
                    self.colors["positive"],
                    self.colors["highlight"]
                ],
                margin=dict(t=80, l=50, r=50, b=50)
            )
        )
        pio.templates.default = "consulting"

    def save_image(self, fig: go.Figure, filename: str) -> str:
        """Save figure as high-resolution PNG."""
        output_path = os.path.join(self.output_dir, filename)
        # Use scale=3 for high DPI (300 equivalent)
        fig.write_image(output_path, scale=3, width=1000, height=600, engine="kaleido")
        print(f"VisualEngine: Saved chart to {output_path}")
        return output_path

    def generate_waterfall(self, 
                          categories: List[str], 
                          values: List[float], 
                          title: str, 
                          filename: str,
                          measures: Optional[List[str]] = None) -> str:
        """
        Generate a Waterfall chart (e.g., EBITDA bridge).
        """
        print(f"VisualEngine: Generating Waterfall '{title}'...")
        
        # Auto-calculate measures if not provided (assume all 'relative' except last 'total')
        if not measures:
            measures = ["relative"] * (len(values) - 1) + ["total"]
            
        # Determine colors based on value (Green for +, Red for -)
        colors = []
        for v, m in zip(values, measures):
            if m == "total":
                colors.append(self.colors["primary"])
            elif v >= 0:
                colors.append(self.colors["positive"])
            else:
                colors.append(self.colors["highlight"])

        fig = go.Figure(go.Waterfall(
            name="20", orientation="v",
            measure=measures,
            x=categories,
            textposition="outside",
            text=[f"{v:+.1f}" if m != "total" else f"{v:.1f}" for v, m in zip(values, measures)],
            y=values,
            connector={"line": {"color": self.colors["accent"]}},
            decreasing={"marker": {"color": self.colors["highlight"]}},
            increasing={"marker": {"color": self.colors["positive"]}},
            totals={"marker": {"color": self.colors["primary"]}}
        ))

        fig.update_layout(title_text=title, showlegend=False)
        return self.save_image(fig, filename)

    def generate_sankey(self, 
                       labels: List[str], 
                       source: List[int], 
                       target: List[int], 
                       values: List[float], 
                       title: str, 
                       filename: str) -> str:
        """
        Generate a Sankey diagram for flow analysis.
        """
        print(f"VisualEngine: Generating Sankey '{title}'...")
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=self.colors["primary"]
            ),
            link=dict(
                source=source,
                target=target,
                value=values,
                color="rgba(0, 32, 96, 0.2)" # Semi-transparent primary
            )
        )])

        fig.update_layout(title_text=title, font_size=12)
        return self.save_image(fig, filename)

    def generate_heatmap(self, 
                        data: List[List[float]], 
                        x_labels: List[str], 
                        y_labels: List[str], 
                        title: str, 
                        filename: str) -> str:
        """
        Generate a Heatmap (e.g., Risk Matrix, Correlation).
        """
        print(f"VisualEngine: Generating Heatmap '{title}'...")
        
        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=x_labels,
            y=y_labels,
            colorscale="Blues", # Professional blue gradient
            text=data,
            texttemplate="%{text:.1f}",
            textfont={"size": 12}
        ))

        fig.update_layout(title_text=title)
        return self.save_image(fig, filename)

    def generate_treemap(self, 
                        labels: List[str], 
                        parents: List[str], 
                        values: List[float], 
                        title: str, 
                        filename: str) -> str:
        """
        Generate a Treemap for hierarchical data.
        """
        print(f"VisualEngine: Generating Treemap '{title}'...")
        
        fig = go.Figure(go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            textinfo="label+value+percent parent",
            marker=dict(colorscale="Blues")
        ))

        fig.update_layout(title_text=title)
        return self.save_image(fig, filename)

    def generate_radar(self, 
                      categories: List[str], 
                      data: Dict[str, List[float]], 
                      title: str, 
                      filename: str) -> str:
        """
        Generate a Radar Chart (Spider Chart) for skill/capability assessment.
        """
        print(f"VisualEngine: Generating Radar Chart '{title}'...")
        
        fig = go.Figure()

        for name, values in data.items():
            # Close the loop
            r_values = values + [values[0]]
            theta_values = categories + [categories[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=r_values,
                theta=theta_values,
                fill='toself',
                name=name
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max([max(v) for v in data.values()]) * 1.1]
                )
            ),
            title_text=title,
            showlegend=True
        )
        
        return self.save_image(fig, filename)

    def generate_bar_chart(self, 
                          data: Dict[str, float], 
                          title: str, 
                          filename: str,
                          orientation: str = 'v') -> str:
        """Standard Bar Chart with premium styling."""
        print(f"VisualEngine: Generating Bar Chart '{title}'...")
        
        x = list(data.keys())
        y = list(data.values())
        
        if orientation == 'h':
            fig = go.Figure(go.Bar(
                x=y, y=x, orientation='h',
                marker_color=self.colors["primary"],
                text=y, textposition='auto'
            ))
        else:
            fig = go.Figure(go.Bar(
                x=x, y=y,
                marker_color=self.colors["primary"],
                text=y, textposition='auto'
            ))

        fig.update_layout(title_text=title)
        return self.save_image(fig, filename)

    def generate_line_chart(self, 
                           data: Dict[str, List[float]], 
                           x_labels: List[str],
                           title: str, 
                           filename: str) -> str:
        """Standard Line Chart with premium styling."""
        print(f"VisualEngine: Generating Line Chart '{title}'...")
        
        fig = go.Figure()
        
        for name, values in data.items():
            fig.add_trace(go.Scatter(
                x=x_labels, y=values,
                mode='lines+markers',
                name=name,
                line=dict(width=3)
            ))

        fig.update_layout(title_text=title, showlegend=True)
        return self.save_image(fig, filename)

    def generate_donut_chart(self, 
                            data: Dict[str, float], 
                            title: str, 
                            filename: str) -> str:
        """Donut Chart (Modern Pie)."""
        print(f"VisualEngine: Generating Donut Chart '{title}'...")
        
        labels = list(data.keys())
        values = list(data.values())
        
        fig = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=.4, # Donut style
            textinfo='label+percent',
            marker=dict(colors=[self.colors["primary"], self.colors["secondary"], 
                              self.colors["accent"], self.colors["positive"]])
        )])

        fig.update_layout(title_text=title)
        return self.save_image(fig, filename)
