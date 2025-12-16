
import json
import sys
import os

# Add root directory to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.services.gap_analysis import SmartWorkloadAnalyzer

def run_verification():
    print("=== Smart Gap Analysis Verification ===\n")
    
    analyzer = SmartWorkloadAnalyzer()
    
    # Test Data: Mixed English and Korean, scattered tasks
    mock_tasks = [
        # Admin Tasks
        {"id": "1", "task_name": "Review daily emails", "fte": 0.2, "action_verb": "review"},
        {"id": "2", "task_name": "이메일 회신 및 관리", "fte": 0.3, "action_verb": "manage"},
        {"id": "3", "task_name": "Schedule team meetings", "fte": 0.1, "action_verb": "schedule"},
        {"id": "4", "task_name": "회의실 예약 및 일정 조율", "fte": 0.1, "action_verb": "coordinate"},
        
        # Strategy Tasks
        {"id": "5", "task_name": "Develop 2025 Strategic Roadmap", "fte": 0.4, "action_verb": "develop"},
        {"id": "6", "task_name": "신사업 기획안 작성", "fte": 0.3, "action_verb": "plan"},
        {"id": "7", "task_name": "비전 선포식 준비", "fte": 0.2, "action_verb": "prepare"},
        
        # Tech Tasks (Overloaded)
        {"id": "8", "task_name": "Backend API Optimization", "fte": 0.5, "action_verb": "optimize"},
        {"id": "9", "task_name": "대용량 데이터 마이그레이션", "fte": 0.4, "action_verb": "migrate"},
        {"id": "10", "task_name": "Server Log Analysis", "fte": 0.4, "action_verb": "analyze"},
        
        # Random Task
        {"id": "11", "task_name": "Office Plant Watering", "fte": 0.05, "action_verb": "water"}
    ]
    
    print(f"Input: {len(mock_tasks)} Raw Tasks")
    print("-" * 50)
    
    # Run Analysis
    results = analyzer.cluster_tasks(mock_tasks)
    
    # Display Results
    for i, cluster in enumerate(results):
        print(f"\n[Cluster {i+1}] {cluster['duty_name']}")
        print(f"Total FTE: {cluster['fte_sum']} ({cluster['fte_sum']*100:.0f}%)")
        print(f"Recommendation: {cluster['recommendation']}")
        print("Included Tasks:")
        for t in cluster['tasks']:
            print(f" - [{t['task_name']}] (FTE: {t['fte']})")
            
    print("\n" + "="*50)
    
    # Assertions
    # 1. Total FTE preservation
    input_fte = sum(t['fte'] for t in mock_tasks)
    output_fte = sum(c['fte_sum'] for c in results)
    print(f"\nVerification Stats:")
    print(f"Input Total FTE: {input_fte:.2f}")
    print(f"Output Total FTE: {output_fte:.2f}")
    
    if abs(input_fte - output_fte) < 0.001:
        print("[SUCCESS] Total FTE Preserved")
    else:
        print("[FAIL] FTE Mismatch")
        
    # Check if 'Admin' or '행정' related grouping happened
    admin_group = next((c for c in results if "행정" in c['duty_name'] or "General" in c['duty_name']), None)
    if admin_group:
        print("[SUCCESS] Admin tasks identified")
    else:
        print("[WARNING] Admin tasks might not be identified ideally")

    # Check validation message for high workload
    overload_group = next((c for c in results if c['fte_sum'] > 1.2), None)
    if overload_group and ("과부하" in overload_group['recommendation'] or "Buy" in overload_group['recommendation']):
        print("[SUCCESS] Overload validation verified")
    else:
        print("[FAIL] Overload validation missed")

if __name__ == "__main__":
    run_verification()
