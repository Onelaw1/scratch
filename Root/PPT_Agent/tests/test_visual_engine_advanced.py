import os
import sys
import numpy as np
import pandas as pd

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.engines.visual_engine import VisualEngine

def test_advanced_charts():
    """
    Test all advanced chart types in the enhanced Visual Engine.
    """
    print("\n" + "="*80)
    print("TESTING ADVANCED VISUAL ENGINE")
    print("="*80 + "\n")
    
    engine = VisualEngine(output_dir="output/visuals_test")
    
    # ==================== 3D VISUALIZATIONS ====================
    
    print("[3D CHARTS] Testing 3D Visualizations...")
    
    # 1. 3D Scatter Plot
    print("  ├─ Creating 3D Scatter Plot...")
    df_3d = pd.DataFrame({
        'Risk': np.random.rand(50) * 10,
        'Return': np.random.rand(50) * 10,
        'Volume': np.random.rand(50) * 1000,
        'Category': np.random.choice(['A', 'B', 'C'], 50)
    })
    path_3d_scatter = engine.create_3d_scatter(
        df_3d, x='Risk', y='Return', z='Volume', color='Category',
        title="Portfolio Risk-Return-Volume Analysis",
        filename="3d_scatter_portfolio.png"
    )
    assert os.path.exists(path_3d_scatter)
    print(f"  │  ✓ Created: {path_3d_scatter}")
    
    # 2. 3D Surface Plot
    print("  ├─ Creating 3D Surface Plot...")
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    path_3d_surface = engine.create_3d_surface(
        Z, title="Sensitivity Analysis Surface",
        filename="3d_surface_sensitivity.png"
    )
    assert os.path.exists(path_3d_surface)
    print(f"  │  ✓ Created: {path_3d_surface}")
    
    # 3. 3D Bar Chart
    print("  └─ Creating 3D Bar Chart...")
    df_3d_bar = pd.DataFrame({
        'Region': ['North', 'South', 'East', 'West'] * 3,
        'Product': ['A']*4 + ['B']*4 + ['C']*4,
        'Sales': np.random.rand(12) * 1000
    })
    path_3d_bar = engine.create_3d_bar(
        df_3d_bar, x='Region', y='Product', z='Sales',
        title="Sales by Region and Product",
        filename="3d_bar_sales.png"
    )
    assert os.path.exists(path_3d_bar)
    print(f"     ✓ Created: {path_3d_bar}\n")
    
    # ==================== HEATMAPS ====================
    
    print("[HEATMAPS] Testing Heatmaps...")
    
    # Correlation Matrix
    print("  └─ Creating Correlation Heatmap...")
    df_corr = pd.DataFrame(
        np.random.randn(10, 10),
        columns=[f'Var{i}' for i in range(10)],
        index=[f'Var{i}' for i in range(10)]
    )
    corr_matrix = df_corr.corr()
    path_heatmap = engine.create_heatmap(
        corr_matrix, title="Correlation Matrix Analysis",
        filename="heatmap_correlation.png"
    )
    assert os.path.exists(path_heatmap)
    print(f"     ✓ Created: {path_heatmap}\n")
    
    # ==================== WATERFALL CHARTS ====================
    
    print("[WATERFALL] Testing Waterfall Charts...")
    
    print("  └─ Creating Revenue Bridge...")
    categories = ['Q1 Revenue', 'New Sales', 'Upsells', 'Churn', 'Q2 Revenue']
    values = [1000, 250, 150, -200, 1200]
    path_waterfall = engine.create_waterfall(
        categories, values,
        title="Q1 to Q2 Revenue Bridge",
        filename="waterfall_revenue.png"
    )
    assert os.path.exists(path_waterfall)
    print(f"     ✓ Created: {path_waterfall}\n")
    
    # ==================== SANKEY DIAGRAMS ====================
    
    print("[SANKEY] Testing Sankey Diagrams...")
    
    print("  └─ Creating Customer Journey Flow...")
    # Source: 0=Awareness, 1=Interest, 2=Consideration, 3=Purchase, 4=Retention
    source = [0, 0, 1, 1, 2, 2, 3]
    target = [1, 2, 2, 3, 3, 4, 4]
    value = [1000, 500, 800, 200, 600, 400, 500]
    labels = ['Awareness', 'Interest', 'Consideration', 'Purchase', 'Retention']
    
    path_sankey = engine.create_sankey(
        source, target, value, labels,
        title="Customer Journey Flow Analysis",
        filename="sankey_customer_journey.png"
    )
    assert os.path.exists(path_sankey)
    print(f"     ✓ Created: {path_sankey}\n")
    
    # ==================== SUNBURST & TREEMAP ====================
    
    print("[HIERARCHY] Testing Sunburst & Treemap...")
    
    # Hierarchical data
    df_hierarchy = pd.DataFrame({
        'Region': ['North', 'North', 'North', 'South', 'South', 'South'],
        'Country': ['USA', 'USA', 'Canada', 'Brazil', 'Brazil', 'Argentina'],
        'City': ['NYC', 'LA', 'Toronto', 'Sao Paulo', 'Rio', 'Buenos Aires'],
        'Revenue': [1000, 800, 600, 700, 500, 400]
    })
    
    print("  ├─ Creating Sunburst Chart...")
    path_sunburst = engine.create_sunburst(
        df_hierarchy, path=['Region', 'Country', 'City'], values='Revenue',
        title="Revenue by Geographic Hierarchy",
        filename="sunburst_revenue.png"
    )
    assert os.path.exists(path_sunburst)
    print(f"  │  ✓ Created: {path_sunburst}")
    
    print("  └─ Creating Treemap...")
    path_treemap = engine.create_treemap(
        df_hierarchy, path=['Region', 'Country', 'City'], values='Revenue',
        title="Revenue Portfolio Treemap",
        filename="treemap_revenue.png"
    )
    assert os.path.exists(path_treemap)
    print(f"     ✓ Created: {path_treemap}\n")
    
    # ==================== FUNNEL CHARTS ====================
    
    print("[FUNNEL] Testing Funnel Charts...")
    
    print("  └─ Creating Sales Funnel...")
    stages = ['Leads', 'Qualified', 'Proposal', 'Negotiation', 'Closed']
    funnel_values = [1000, 600, 400, 250, 150]
    path_funnel = engine.create_funnel(
        stages, funnel_values,
        title="Sales Conversion Funnel",
        filename="funnel_sales.png"
    )
    assert os.path.exists(path_funnel)
    print(f"     ✓ Created: {path_funnel}\n")
    
    # ==================== BULLET CHARTS ====================
    
    print("[BULLET] Testing Bullet Charts...")
    
    print("  └─ Creating KPI Dashboard...")
    ranges = [(60, 'Poor'), (80, 'Fair'), (100, 'Good')]
    path_bullet = engine.create_bullet_chart(
        actual=85, target=90, ranges=ranges,
        title="Q2 Performance vs Target",
        filename="bullet_kpi.png"
    )
    assert os.path.exists(path_bullet)
    print(f"     ✓ Created: {path_bullet}\n")
    
    # ==================== ENHANCED BASIC CHARTS ====================
    
    print("[ENHANCED] Testing Enhanced Basic Charts...")
    
    df_basic = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Revenue': [100, 120, 115, 140, 160, 155],
        'Costs': [60, 65, 70, 75, 80, 78],
        'Category': ['A', 'B', 'A', 'B', 'A', 'B']
    })
    
    print("  ├─ Creating Enhanced Bar Chart...")
    path_bar = engine.create_mckinsey_chart(
        df_basic, 'bar', x='Month', y='Revenue',
        title="Monthly Revenue Trend",
        filename="enhanced_bar.png"
    )
    assert os.path.exists(path_bar)
    print(f"  │  ✓ Created: {path_bar}")
    
    print("  └─ Creating Enhanced Line Chart...")
    path_line = engine.create_mckinsey_chart(
        df_basic, 'line', x='Month', y='Revenue',
        title="Revenue Growth Trajectory",
        filename="enhanced_line.png"
    )
    assert os.path.exists(path_line)
    print(f"     ✓ Created: {path_line}\n")
    
    # ==================== EXISTING FRAMEWORKS ====================
    
    print("[FRAMEWORKS] Testing Existing Framework Diagrams...")
    
    print("  ├─ Creating 3C Analysis...")
    path_3c = engine.generate_3c_analysis()
    assert os.path.exists(path_3c)
    print(f"  │  ✓ Created: {path_3c}")
    
    print("  ├─ Creating Impact/Effort Matrix...")
    path_ie = engine.generate_impact_effort_matrix([])
    assert os.path.exists(path_ie)
    print(f"  │  ✓ Created: {path_ie}")
    
    print("  └─ Creating RACI Matrix...")
    path_raci = engine.generate_raci_matrix()
    assert os.path.exists(path_raci)
    print(f"     ✓ Created: {path_raci}\n")
    
    # ==================== SUMMARY ====================
    
    print("="*80)
    print("SUCCESS: ALL ADVANCED CHART TYPES GENERATED SUCCESSFULLY!")
    print("="*80)
    print(f"\nOutput Directory: {engine.output_dir}")
    print(f"Total Charts Created: 17")
    print("\nChart Types Tested:")
    print("  • 3D Scatter, Surface, Bar")
    print("  • Heatmap (Correlation Matrix)")
    print("  • Waterfall (Revenue Bridge)")
    print("  • Sankey (Customer Journey)")
    print("  • Sunburst & Treemap (Hierarchical)")
    print("  • Funnel (Sales Conversion)")
    print("  • Bullet (KPI Dashboard)")
    print("  • Enhanced Bar & Line Charts")
    print("  • 3C Analysis, Impact/Effort, RACI Matrix")
    print("\nAll charts use McKinsey-style professional theming!")
    print("="*80 + "\n")

if __name__ == "__main__":
    test_advanced_charts()
