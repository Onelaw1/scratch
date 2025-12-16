from typing import List, Optional, Literal, Dict, Any, Union
from pydantic import BaseModel, Field

class TextStyle(BaseModel):
    is_bold: bool = False
    color_hex: Optional[str] = None
    font_size: Optional[int] = None
    background_hex: Optional[str] = None

class ContentBlock(BaseModel):
    block_type: Literal["text", "table", "chart", "image", "kpi_card"]
    content: str = Field(..., description="The actual text content or description of visual element")
    position: str = Field(..., description="Position description e.g. top-left, step-1, etc.")
    style: Optional[TextStyle] = None

class Section(BaseModel):
    title: Optional[str] = None
    layout_type: Optional[str] = None # roof, columns_3, process_flow, etc.
    blocks: List[ContentBlock] = []

class FrameworkElement(BaseModel):
    label: str
    description: Optional[str] = None
    position: Optional[str] = None

class ContentData(BaseModel):
    # Cover fields
    subtitle: Optional[str] = None
    date: Optional[str] = None
    client_name: Optional[str] = None
    
    # Framework fields
    framework_type: Optional[Literal["2x2", "Process", "Pyramid", "List", "StrategyHouse"]] = None
    elements: Optional[List[FrameworkElement]] = None
    
    # Content/Data fields
    sections: Optional[List[Section]] = None

class SlideLayout(BaseModel):
    grid_type: Literal["1-column", "2-column", "3-column", "2x2-grid", "custom"]
    background_color: Optional[str] = "#FFFFFF"

class JangpyoSlide(BaseModel):
    """
    Represents a single high-density report slide.
    """
    slide_type: Literal["Cover", "Framework", "Content", "Data"] = Field(..., description="The semantic type of the slide")
    slide_number: int
    
    # L0: Slide Title (Top left usually)
    title: str = Field(..., description="The main subject of the slide (L0)")
    
    # L1: Governing Message (The 'So What')
    governing_message: Optional[str] = Field(None, description="The full sentence conclusion at the top (L1)")
    
    layout: SlideLayout
    
    # Flexible content data
    content_data: ContentData
    
    # Footer / Sources
    footer: Optional[str] = None
    
    def to_prompt_format(self) -> str:
        return self.model_dump_json(indent=2)

class ReportDeck(BaseModel):
    title: str
    slides: List[JangpyoSlide]
