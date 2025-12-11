import json
from pathlib import Path

class PromptEngine:
    def __init__(self, persona_path: str = "config/persona_config.json", style_guide_path: str = "config/style_guide.md"):
        self.persona = self._load_json(persona_path)
        self.style_guide = self._load_text(style_guide_path)

    def _load_json(self, path: str) -> dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _load_text(self, path: str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def get_system_prompt(self) -> str:
        """
        Constructs the system prompt for the Vision AI.
        """
        role = self.persona.get("role", "Consultant")
        tone = self.persona.get("tone", {})
        vocab = self.persona.get("vocabulary", {})
        
        prompt = f"""
You are a {role} expert in creating "Jangpyo" (High-Density Strategic Reports).
Your goal is to analyze the provided image of a report slide and deconstruct it into a structured JSON format.

## YOUR PERSONA
- Tone: {tone.get("professionalism", "Professional")} and {tone.get("style", "MECE")}
- Vocabulary to Use: {", ".join(vocab.get("preferred_terms", []))}
- Vocabulary to AVOID: {", ".join(vocab.get("avoid_terms", []))}

## CRITICAL INSTRUCTIONS
1. **Company Name Filtering**: You must **REMOVE** any mention of "Ryan & Co", "Ryan&Co", or "RNC" from the output. Do not include logos or text containing these names.
2. **Structure Recognition**: You must identify the VISUAL STRUCTURE of the slide. Do not just extract text. Look for:
   - **Strategy House**: A roof (triangle) on top, pillars (columns) in the middle, and a foundation (rectangle) at the bottom.
   - **Process Flow**: Steps connected by arrows or chevrons (e.g., Step 1 -> Step 2 -> Step 3).
   - **3-Column List**: Three distinct vertical columns with titles.
   - **Tables/Charts**: Explicit data grids or graphs.

3. **Slide Classification**:
   - `Cover`: Title page.
   - `Framework`: Slide with a specific visual model (Strategy House, Process Flow).
   - `Content`: Text/bullet points.
   - `Data`: Charts/Tables.

## OUTPUT FORMAT
You must output VALID JSON matching the following schema.

{{
  "slide_type": "Cover" | "Framework" | "Content" | "Data",
  "slide_number": int,
  "title": "string (L0 Title)",
  "governing_message": "string (L1 Message)",
  "layout": {{
    "grid_type": "1-column" | "2-column" | "3-column" | "custom",
    "background_color": "string (hex)"
  }},
  "content_data": {{
    // IF slide_type == "Cover"
    "subtitle": "string",
    "date": "string",
    "client_name": "string",
    
    // IF slide_type == "Framework"
    "framework_type": "StrategyHouse" | "Process" | "Pyramid" | "List",
    
    // COMMON SECTIONS (Used for Frameworks, Content, and Data)
    "sections": [
       {{
         "title": "string (Section Title)",
         "layout_type": "roof" | "columns_3" | "process_flow" | "full_width" | "generic",
         "blocks": [
           {{
             "block_type": "text" | "table" | "chart" | "image" | "kpi_card",
             "content": "string (For tables, use Markdown format. For charts, describe data trends)",
             "position": "top-left" | "top-right" | "bottom-left" | "bottom-right" | "center" | "full-width",
             "style": {{ "is_bold": boolean, "color_hex": "string", "font_size": int, "background_hex": "string" }}
           }}
         ]
       }}
    ]
  }},
  "footer": "string"
}}

## VISUAL CUES FOR LAYOUT_TYPE
- If you see a **Triangle** or "Vision/Mission" block at the top -> `layout_type: "roof"`
- If you see **3 Vertical Boxes** side-by-side -> `layout_type: "columns_3"`
- If you see **Chevrons/Arrows** (Step 1, Step 2...) -> `layout_type: "process_flow"`
- If you see a wide box at the bottom (Foundation) -> `layout_type: "full_width"`

- Do not include markdown formatting like ```json ... ``` in your response, just the raw JSON.
"""
        return prompt
