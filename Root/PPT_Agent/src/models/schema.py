from typing import List, Optional
from pydantic import BaseModel, Field

class SlideContent(BaseModel):
    title: str = Field(..., description="Title of the slide")
    bullet_points: List[str] = Field(default_factory=list, description="List of bullet points")
    image_description: Optional[str] = Field(None, description="Description of an image to include")
    speaker_notes: Optional[str] = Field(None, description="Speaker notes for the slide")

class PresentationSchema(BaseModel):
    topic: str = Field(..., description="Topic of the presentation")
    slides: List[SlideContent] = Field(..., description="List of slides in the presentation")
