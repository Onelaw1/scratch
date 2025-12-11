from src.models.schema import SlideContent

class DesignerAgent:
    def __init__(self):
        pass

    def design_slide(self, content: SlideContent) -> dict:
        """
        Determines the layout and styling for a slide.
        """
        print(f"Designer: Designing layout for '{content.title}'...")
        
        # Layout Logic
        layout_index = 1
        if "Introduction" in content.title or "Title" in content.title:
            layout_index = 0
            
        # Style Logic (Simple Keyword Matching)
        # Default: Clean White/Grey
        theme = {
            "font_family": "Calibri",
            "title_color": (0, 0, 0),       # Black
            "body_color": (89, 89, 89),     # Dark Grey
            "background_color": (255, 255, 255) # White
        }
        
        # Dark Mode for "Future", "AI", "Tech"
        keywords = ["Future", "AI", "Tech", "Cyber", "Digital"]
        if any(k in content.title for k in keywords) or any(k in str(content.bullet_points) for k in keywords):
            theme = {
                "font_family": "Arial", # PowerPoint standard safe font
                "title_color": (0, 255, 255),   # Cyan
                "body_color": (200, 200, 200),  # Light Grey
                "background_color": (20, 20, 30) # Dark Blue/Black
            }
            
        return {
            "layout_index": layout_index,
            **theme
        }
