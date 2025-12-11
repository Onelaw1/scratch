import sys
import os
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src.agents.planner import PlannerAgent
from src.services.memory_service import MemoryService

def test_planner():
    try:
        # 1. Seed Memory with Persona
        print("Initializing Memory Service...")
        memory = MemoryService()
        memory.seed_initial_persona()
        
        # 2. Initialize Agent
        agent = PlannerAgent()
        topic = "Strategy for ESG Implementation in Public Institutions"
        print(f"\nTesting Planner Agent with topic: {topic}")
        
        # 3. Generate Plan (Triggering Dialectic Loop)
        plan = agent.plan_presentation(topic)
        
        print("\n--- Final Generated Plan ---")
        print(f"Topic: {plan.topic}")
        for i, slide in enumerate(plan.slides, 1):
            print(f"\nSlide {i}: {slide.title}")
            for bp in slide.bullet_points:
                print(f"  - {bp}")
        
        print("\n--- Verification ---")
        # Check for Evaluator-Centric keywords (Academic Rigor & Compliance)
        evaluator_keywords = ["Manual", "Indicator", "Evidence", "Compliance", "Quantitative", "Evaluation"]
        
        content_str = str(plan.slides)
        found_keywords = [k for k in evaluator_keywords if k.lower() in content_str.lower()]
        
        print(f"Evaluator Keywords Found: {found_keywords}")
        
        if len(found_keywords) >= 2:
            print("SUCCESS: Plan reflects 'Evaluator-Centric' standards (Compliance + Evidence).")
        else:
            print("WARNING: Plan lacks academic rigor or manual references.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_planner()
