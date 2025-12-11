import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import vizro.plotly.express as vpx
from vizro import Vizro
import vizro.models as vm
from html2image import Html2Image
import os
import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple, Any

class VisualEngine:
    """
    Advanced Visual Engine for creating Consulting-grade Charts and Diagrams.
    - Charts: Uses Plotly with McKinsey/BCG-style theming
    - Diagrams: Uses HTML/CSS capture for custom visuals
    - Features: 3D charts, heatmaps, waterfall, Sankey, geographic maps
    """

    # McKinsey Color Palette
    MCKINSEY_BLUE = '#005A9C'
    MCKINSEY_LIGHT_BLUE = '#00A3E0'
    MCKINSEY_DARK_BLUE = '#003D6A'
    BCG_GREEN = '#6A994E'
    BAIN_ORANGE = '#F18F01'
    ACCENT_RED = '#C73E1D'
    ACCENT_PURPLE = '#A23B72'
    NEUTRAL_GRAY = '#7F7F7F'
    
    # Professional Color Schemes
    SEQUENTIAL_BLUES = ['#E6F2FF', '#99CCFF', '#4D94FF', '#005A9C', '#003D6A']
    DIVERGING = ['#C73E1D', '#F18F01', '#EEEEEE', '#00A3E0', '#005A9C']
    CATEGORICAL = [MCKINSEY_BLUE, BCG_GREEN, BAIN_ORANGE, ACCENT_PURPLE, ACCENT_RED, NEUTRAL_GRAY]

    def __init__(self, output_dir: str = "output/visuals"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.hti = Html2Image(output_path=self.output_dir)
        
    def _apply_mckinsey_theme(self, fig: go.Figure, title: str = "") -> go.Figure:
        """
        Apply McKinsey-style professional theming to any Plotly figure.
        """
        fig.update_layout(
            # Typography
            font_family="Arial, Helvetica, sans-serif",
            font_color="#333333",
            title_font_size=24,
            title_font_color="#000000",
            title_x=0.0,  # Left-aligned
            title_font_weight="bold",
            
            # Legend
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                font=dict(size=11),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="#CCCCCC",
                borderwidth=1
            ),
            
            # Plot background
            plot_bgcolor="white",
            paper_bgcolor="white",
            
            # Margins
            margin=dict(l=60, r=120, t=80, b=60),
            
            # Grid
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#E5E5E5',
                showline=True,
                linewidth=2,
                linecolor='#333333',
                mirror=False,
                ticks='outside',
                tickfont=dict(size=11, color='#333333')
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#E5E5E5',
                showline=True,
                linewidth=2,
                linecolor='#333333',
                mirror=False,
                ticks='outside',
                tickfont=dict(size=11, color='#333333')
            ),
            
            # Hover
            hovermode='closest',
            hoverlabel=dict(
                bgcolor="white",
                font_size=11,
                font_family="Arial"
            )
        )
        
        return fig
    
    def _save_figure(self, fig: go.Figure, filename: str, width: int = 1920, height: int = 1080) -> str:
        """
        Save Plotly figure as high-resolution PNG.
        """
        output_path = os.path.join(self.output_dir, filename)
        fig.write_image(output_path, width=width, height=height, scale=2)
        return output_path

    # ==================== 3D VISUALIZATIONS ====================
    
    def create_3d_scatter(self, df: pd.DataFrame, x: str, y: str, z: str, 
                          color: Optional[str] = None, size: Optional[str] = None,
                          title: str = "3D Scatter Plot", filename: str = "3d_scatter.png") -> str:
        """
        Create 3D scatter plot for multi-dimensional data analysis.
        Perfect for: Portfolio analysis, risk-return-volume analysis, multi-factor analysis
        """
        fig = px.scatter_3d(
            df, x=x, y=y, z=z, color=color, size=size,
            title=title,
            color_discrete_sequence=self.CATEGORICAL
        )
        
        fig.update_traces(
            marker=dict(
                line=dict(width=0.5, color='white'),
                opacity=0.8
            )
        )
        
        fig = self._apply_mckinsey_theme(fig, title)
        return self._save_figure(fig, filename)
    
    def create_3d_surface(self, z_data: np.ndarray, x_labels: List = None, y_labels: List = None,
                          title: str = "3D Surface Plot", filename: str = "3d_surface.png") -> str:
        """
        Create 3D surface plot for continuous data visualization.
        Perfect for: Sensitivity analysis, optimization landscapes, response surfaces
        """
        fig = go.Figure(data=[go.Surface(
            z=z_data,
            colorscale='Blues',
            colorbar=dict(title="Value", thickness=20, len=0.7)
        )])
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis=dict(title="X Axis", backgroundcolor="white", gridcolor="#E5E5E5"),
                yaxis=dict(title="Y Axis", backgroundcolor="white", gridcolor="#E5E5E5"),
                zaxis=dict(title="Z Axis", backgroundcolor="white", gridcolor="#E5E5E5"),
            ),
            font_family="Arial"
        )
        
        return self._save_figure(fig, filename)
    
    def create_3d_bar(self, df: pd.DataFrame, x: str, y: str, z: str,
                      title: str = "3D Bar Chart", filename: str = "3d_bar.png") -> str:
        """
        Create 3D bar chart for categorical data across two dimensions.
        Perfect for: Market share by region and product, performance by department and quarter
        """
        fig = px.bar_3d(df, x=x, y=y, z=z, title=title, color=z,
                        color_continuous_scale='Blues')
        
        fig = self._apply_mckinsey_theme(fig, title)
        return self._save_figure(fig, filename)

    # ==================== HEATMAPS ====================
    
    def create_heatmap(self, df: pd.DataFrame, title: str = "Heatmap Analysis",
                       filename: str = "heatmap.png", annotate: bool = True) -> str:
        """
        Create professional heatmap for correlation matrices, performance grids, etc.
        Perfect for: Correlation analysis, risk matrices, performance dashboards
        """
        fig = go.Figure(data=go.Heatmap(
            z=df.values,
            x=df.columns.tolist(),
            y=df.index.tolist(),
            colorscale='RdBu_r',
            zmid=0,
            text=df.values if annotate else None,
            texttemplate='%{text:.2f}' if annotate else None,
            textfont={"size": 10},
            colorbar=dict(title="Value", thickness=20, len=0.7)
        ))
        
        fig.update_layout(
            title=title,
            xaxis=dict(side='bottom', tickangle=-45),
            yaxis=dict(side='left'),
            font_family="Arial"
        )
        
        return self._save_figure(fig, filename)

    # ==================== WATERFALL CHARTS ====================
    
    def create_waterfall(self, categories: List[str], values: List[float],
                         title: str = "Waterfall Analysis", filename: str = "waterfall.png") -> str:
        """
        Create waterfall chart for variance analysis, financial bridges, etc.
        Perfect for: Revenue bridges, cost breakdowns, P&L variance analysis
        """
        # Determine measure types (relative, total, absolute)
        measure = ["relative"] * (len(categories) - 1) + ["total"]
        
        fig = go.Figure(go.Waterfall(
            name="",
            orientation="v",
            measure=measure,
            x=categories,
            y=values,
            connector={"line": {"color": "#7F7F7F", "width": 2, "dash": "dot"}},
            increasing={"marker": {"color": self.BCG_GREEN}},
            decreasing={"marker": {"color": self.ACCENT_RED}},
            totals={"marker": {"color": self.MCKINSEY_BLUE}}
        ))
        
        fig = self._apply_mckinsey_theme(fig, title)
        return self._save_figure(fig, filename)

    # ==================== SANKEY DIAGRAMS ====================
    
    def create_sankey(self, source: List[int], target: List[int], value: List[float],
                      labels: List[str], title: str = "Flow Analysis",
                      filename: str = "sankey.png") -> str:
        """
        Create Sankey diagram for flow visualization.
        Perfect for: Customer journey, budget allocation, process flows, value streams
        """
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="white", width=2),
                label=labels,
                color=self.MCKINSEY_BLUE
            ),
            link=dict(
                source=source,
                target=target,
                value=value,
                color="rgba(0, 90, 156, 0.3)"
            )
        )])
        
        fig.update_layout(
            title=title,
            font=dict(size=12, family="Arial"),
            height=600
        )
        
        return self._save_figure(fig, filename, height=600)

    # ==================== SUNBURST & TREEMAP ====================
    
    def create_sunburst(self, df: pd.DataFrame, path: List[str], values: str,
                        title: str = "Hierarchical Analysis", filename: str = "sunburst.png") -> str:
        """
        Create sunburst chart for hierarchical data.
        Perfect for: Organizational structure, budget breakdown, market segmentation
        """
        fig = px.sunburst(
            df, path=path, values=values, title=title,
            color_discrete_sequence=self.CATEGORICAL
        )
        
        fig.update_traces(textinfo="label+percent parent")
        fig.update_layout(font_family="Arial", title_font_size=24)
        
        return self._save_figure(fig, filename)
    
    def create_treemap(self, df: pd.DataFrame, path: List[str], values: str,
                       title: str = "Portfolio View", filename: str = "treemap.png") -> str:
        """
        Create treemap for hierarchical proportions.
        Perfect for: Product portfolio, market share, resource allocation
        """
        fig = px.treemap(
            df, path=path, values=values, title=title,
            color_discrete_sequence=self.CATEGORICAL
        )
        
        fig.update_traces(textinfo="label+value+percent parent")
        fig.update_layout(font_family="Arial", title_font_size=24)
        
        return self._save_figure(fig, filename)

    # ==================== FUNNEL & BULLET CHARTS ====================
    
    def create_funnel(self, stages: List[str], values: List[float],
                      title: str = "Conversion Funnel", filename: str = "funnel.png") -> str:
        """
        Create funnel chart for conversion analysis.
        Perfect for: Sales funnel, customer journey, process efficiency
        """
        fig = go.Figure(go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            marker=dict(color=self.SEQUENTIAL_BLUES)
        ))
        
        fig = self._apply_mckinsey_theme(fig, title)
        return self._save_figure(fig, filename)
    
    def create_bullet_chart(self, actual: float, target: float, ranges: List[Tuple[float, str]],
                            title: str = "KPI Dashboard", filename: str = "bullet.png") -> str:
        """
        Create bullet chart for KPI visualization.
        Perfect for: Performance dashboards, goal tracking, KPI monitoring
        ranges: List of (value, label) tuples for background ranges
        """
        fig = go.Figure()
        
        # Add range bars
        for i, (val, label) in enumerate(ranges):
            fig.add_trace(go.Bar(
                y=[label],
                x=[val],
                orientation='h',
                marker=dict(color=self.SEQUENTIAL_BLUES[i]),
                name=label,
                showlegend=True
            ))
        
        # Add actual bar
        fig.add_trace(go.Bar(
            y=["Performance"],
            x=[actual],
            orientation='h',
            marker=dict(color=self.MCKINSEY_BLUE),
            name="Actual",
            width=0.3
        ))
        
        # Add target line
        fig.add_vline(x=target, line_dash="dash", line_color=self.ACCENT_RED,
                      annotation_text="Target", annotation_position="top")
        
        fig.update_layout(barmode='overlay', title=title)
        fig = self._apply_mckinsey_theme(fig, title)
        
        return self._save_figure(fig, filename)

    # ==================== EXISTING METHODS (ENHANCED) ====================
    
    def create_mckinsey_chart(self, df: pd.DataFrame, chart_type: str, x: str, y: str, 
                              title: str, color: Optional[str] = None,
                              filename: Optional[str] = None) -> str:
        """
        Creates a Plotly chart with McKinsey-style aesthetics.
        Enhanced with automatic chart selection and professional theming.
        """
        if filename is None:
            filename = f"{title.replace(' ', '_').lower()}.png"
        
        # Create chart based on type
        if chart_type == 'bar':
            fig = px.bar(df, x=x, y=y, color=color, title=title,
                        color_discrete_sequence=self.CATEGORICAL)
        elif chart_type == 'line':
            fig = px.line(df, x=x, y=y, color=color, title=title,
                         color_discrete_sequence=self.CATEGORICAL)
        elif chart_type == 'scatter':
            fig = px.scatter(df, x=x, y=y, color=color, title=title,
                           color_discrete_sequence=self.CATEGORICAL)
        elif chart_type == 'area':
            fig = px.area(df, x=x, y=y, color=color, title=title,
                         color_discrete_sequence=self.CATEGORICAL)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        fig = self._apply_mckinsey_theme(fig, title)
        return self._save_figure(fig, filename)

    def create_html_diagram(self, html_content: str, css_content: str, filename: str) -> str:
        """
        Renders HTML/CSS content and captures it as an image.
        This allows for infinite flexibility in creating custom diagrams.
        """
        full_html = f"""
        <html>
        <head>
            <style>
                body {{ margin: 0; padding: 0; background-color: white; }}
                {css_content}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        self.hti.screenshot(html_str=full_html, save_as=filename, size=(1920, 1080))
        return os.path.join(self.output_dir, filename)

    # ==================== EXISTING FRAMEWORK METHODS ====================
    
    def generate_3c_analysis(self, data: dict = None) -> str:
        """
        Generates a 3C Analysis diagram (Customer, Company, Competitor).
        """
        if data is None:
            data = {
                "Customer": ["Needs", "Segmentation", "Growth"],
                "Company": ["Strengths", "Resources", "Brand"],
                "Competitor": ["Market Share", "Strategy", "Weaknesses"]
            }

        css = """
        .container-3c { 
            position: relative; 
            width: 800px; 
            height: 600px; 
            font-family: 'Arial', sans-serif;
            background: white;
        }
        .circle {
            position: absolute;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            opacity: 0.9;
        }
        .circle h2 { margin: 0 0 10px 0; font-size: 24px; }
        .circle ul { list-style: none; padding: 0; margin: 0; font-size: 14px; }
        .circle li { margin: 5px 0; }
        
        .customer { top: 50px; left: 250px; background-color: #005a9c; }
        .company { top: 300px; left: 100px; background-color: #00a3e0; }
        .competitor { top: 300px; left: 400px; background-color: #7f7f7f; }
        
        .intersection {
            position: absolute;
            color: #333;
            font-weight: bold;
            font-size: 16px;
            z-index: 10;
        }
        .strategy { top: 250px; left: 350px; }
        """
        
        def make_list(items):
            return "".join([f"<li>{item}</li>" for item in items])

        html = f"""
        <div class="container-3c">
            <div class="circle customer">
                <h2>Customer</h2>
                <ul>{make_list(data.get('Customer', []))}</ul>
            </div>
            <div class="circle company">
                <h2>Company</h2>
                <ul>{make_list(data.get('Company', []))}</ul>
            </div>
            <div class="circle competitor">
                <h2>Competitor</h2>
                <ul>{make_list(data.get('Competitor', []))}</ul>
            </div>
            <div class="intersection strategy">Strategy</div>
        </div>
        """
        return self.create_html_diagram(html, css, "3c_analysis.png")

    def generate_impact_effort_matrix(self, items: list) -> str:
        """
        Generates an Impact/Effort Matrix using Plotly.
        items: list of dicts with keys 'name', 'impact', 'effort' (0-10 scale)
        """
        if not items:
            items = [
                {"name": "Quick Win", "impact": 8, "effort": 2},
                {"name": "Major Project", "impact": 9, "effort": 8},
                {"name": "Fill-in", "impact": 3, "effort": 2},
                {"name": "Thankless Task", "impact": 2, "effort": 9}
            ]
            
        df = pd.DataFrame(items)
        
        fig = px.scatter(df, x="effort", y="impact", text="name", 
                         title="Impact vs. Effort Matrix",
                         range_x=[0, 10], range_y=[0, 10])
        
        fig.update_traces(textposition='top center', 
                         marker=dict(size=15, color=self.MCKINSEY_BLUE))
        
        # Add Quadrant Lines
        fig.add_hline(y=5, line_dash="dash", line_color="gray")
        fig.add_vline(x=5, line_dash="dash", line_color="gray")
        
        # Add Quadrant Labels
        fig.add_annotation(x=2.5, y=7.5, text="Quick Wins", showarrow=False, 
                          font=dict(size=20, color=self.BCG_GREEN))
        fig.add_annotation(x=7.5, y=7.5, text="Major Projects", showarrow=False, 
                          font=dict(size=20, color=self.BAIN_ORANGE))
        fig.add_annotation(x=2.5, y=2.5, text="Fill-ins", showarrow=False, 
                          font=dict(size=20, color=self.NEUTRAL_GRAY))
        fig.add_annotation(x=7.5, y=2.5, text="Thankless Tasks", showarrow=False, 
                          font=dict(size=20, color=self.ACCENT_RED))
        
        fig.update_layout(
            xaxis_title="Effort (Cost/Time)",
            yaxis_title="Impact (Value/Benefit)"
        )
        
        fig = self._apply_mckinsey_theme(fig, "Impact vs. Effort Matrix")
        return self._save_figure(fig, "impact_effort_matrix.png")

    def generate_raci_matrix(self, data: dict = None) -> str:
        """
        Generates a RACI Matrix diagram.
        data: dict where keys are Tasks and values are dicts of Role: Code (R, A, C, I)
        """
        if data is None:
            data = {
                "Define Requirements": {"PM": "R", "Dev": "C", "Designer": "C", "Client": "A"},
                "Design UI": {"PM": "I", "Dev": "C", "Designer": "R", "Client": "A"},
                "Develop Backend": {"PM": "I", "Dev": "R", "Designer": "I", "Client": "I"},
                "UAT": {"PM": "A", "Dev": "S", "Designer": "S", "Client": "R"}
            }
            
        roles = sorted(list(set(role for task_roles in data.values() for role in task_roles.keys())))
        
        css = """
        table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'Arial', sans-serif;
            font-size: 16px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
        }
        th {
            background-color: #005a9c;
            color: white;
            text-align: left;
        }
        tr:nth-child(even) { background-color: #f2f2f2; }
        .role-header { text-align: center; }
        .code-R { background-color: #ffcccc; font-weight: bold; }
        .code-A { background-color: #ccffcc; font-weight: bold; }
        .code-C { background-color: #ffffcc; font-weight: bold; }
        .code-I { background-color: #e6e6e6; }
        """
        
        header_row = "".join([f"<th class='role-header'>{role}</th>" for role in roles])
        
        rows_html = ""
        for task, assignments in data.items():
            row_cells = f"<td style='text-align:left; font-weight:bold;'>{task}</td>"
            for role in roles:
                code = assignments.get(role, "")
                class_name = f"code-{code}" if code else ""
                row_cells += f"<td class='{class_name}'>{code}</td>"
            rows_html += f"<tr>{row_cells}</tr>"
            
        html = f"""
        <div style="padding: 20px; background: white;">
            <h2 style="font-family: Arial; color: #333;">RACI Matrix</h2>
            <table>
                <thead>
                    <tr>
                        <th>Task / Role</th>
                        {header_row}
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        """
        return self.create_html_diagram(html, css, "raci_matrix.png")
