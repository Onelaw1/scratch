from src.services.chart_service import ChartService
import os

def verify_visual_engine():
    print("Starting Visual Engine Verification...")
    service = ChartService(output_dir="output/verify_charts")
    
    # 1. Bar Chart
    service.generate_bar_chart(
        {"Q1": 100, "Q2": 120, "Q3": 130, "Q4": 150},
        "Quarterly Revenue (Bar)",
        "bar_chart.png"
    )

    # 2. Line Chart
    service.generate_line_chart(
        {
            "Product A": [10, 15, 13, 17, 20],
            "Product B": [8, 10, 12, 11, 15]
        },
        "Sales Trend (Line)",
        "line_chart.png"
    )

    # 3. Donut Chart
    service.generate_pie_chart(
        {"US": 40, "EU": 30, "APAC": 20, "LATAM": 10},
        "Regional Share (Donut)",
        "donut_chart.png"
    )

    # 4. Waterfall Chart (EBITDA Bridge)
    service.generate_waterfall(
        ["Revenue", "COGS", "Gross Margin", "Opex", "EBITDA"],
        [100, -40, 0, -20, 0], # 0s are placeholders for totals/subtotals if calculated, but here we just show flow
        # Actually let's do a proper bridge
        # Start, +Increase, -Decrease, End
        # Let's use the explicit logic in VisualEngine
        "EBITDA Bridge",
        "waterfall_chart.png"
    )
    # Let's retry Waterfall with better data for the bridge effect
    # Start: 100, Sales: +20, Cost: -10, Tax: -5, End: 105
    # VisualEngine logic: measures need to be passed if we want totals. 
    # But ChartService wrapper doesn't expose measures. 
    # VisualEngine defaults to all relative except last=total.
    # So: [100, 20, -10, -5, 105] -> 100(rel), 20(rel), -10(rel), -5(rel), 105(total)
    service.generate_waterfall(
        ["Opening", "Sales", "Costs", "Taxes", "Closing"],
        [100, 20, -30, -10, 80],
        "Cash Flow Bridge",
        "waterfall_bridge.png"
    )

    # 5. Sankey Diagram
    service.generate_sankey(
        ["Source A", "Source B", "Process 1", "Process 2", "Destination"],
        [0, 1, 0, 2, 3], # Source indices
        [2, 3, 3, 4, 4], # Target indices
        [8, 4, 2, 8, 4], # Values
        "Material Flow (Sankey)",
        "sankey_chart.png"
    )

    # 6. Heatmap
    service.generate_heatmap(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        ["Low", "Med", "High"], # X
        ["Low", "Med", "High"], # Y
        "Risk Matrix (Heatmap)",
        "heatmap_chart.png"
    )

    # 7. Treemap
    service.generate_treemap(
        ["Global", "US", "EU", "Asia", "NY", "CA", "London", "Tokyo"],
        ["", "Global", "Global", "Global", "US", "US", "EU", "Asia"],
        [100, 40, 30, 30, 20, 20, 30, 30],
        "Market Structure (Treemap)",
        "treemap_chart.png"
    )

    # 8. Radar Chart
    service.generate_radar(
        ["Strategy", "Operations", "Technology", "People", "Finance"],
        {
            "Company A": [4, 3, 5, 2, 4],
            "Company B": [3, 4, 3, 4, 3]
        },
        "Capability Assessment (Radar)",
        "radar_chart.png"
    )

    print("Verification Complete. Check output/verify_charts/")

if __name__ == "__main__":
    verify_visual_engine()
