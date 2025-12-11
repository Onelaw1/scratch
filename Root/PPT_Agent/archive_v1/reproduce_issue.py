
import os
import sys
from PIL import Image
from src.analysis.vision_agent import VisionAgent

# Create a dummy image
img = Image.new('RGB', (100, 100), color = 'red')

try:
    agent = VisionAgent()
    print("VisionAgent initialized successfully.")
    # We won't call analyze_slide yet as it costs money/quota and we just want to check init first
    # result = agent.analyze_slide(img)
    # print(result)
except Exception as e:
    print(f"Error: {e}")
