from typing import List, Dict, Any
from collections import defaultdict
import math
import re

class SmartWorkloadAnalyzer:
    def __init__(self):
        # Pre-defined duty archetypes for "Auto-Labeling" clusters
        self.duty_keywords = {
            "행정 지원 (Administrative)": ["email", "schedule", "meeting", "filing", "admin", "calendar", "call", "이메일", "일정", "회의", "문서", "행정", "전화", "정리"],
            "전략 기획 (Strategy)": ["strategy", "plan", "vision", "roadmap", "lead", "goal", "budget", "전략", "기획", "비전", "로드맵", "목표", "예산", "리딩"],
            "기술 운영 (Tech Ops)": ["code", "develop", "system", "server", "analysis", "data", "fix", "bug", "api", "backend", "tech", "optimize", "코드", "개발", "시스템", "서버", "분석", "데이터", "수정", "버그", "최적화"],
            "고객 서비스 (CS)": ["client", "customer", "support", "ticket", "service", "complaint", "고객", "지원", "티켓", "민원", "서비스", "응대"]
        }

    def _tokenize(self, text: str) -> set:
        text = text.lower()
        # Support English and Korean
        # English: 2+ chars
        # Korean: 1+ chars (as 1 char can be meaningful e.g. '팀')
        tokens_en = re.findall(r'\b[a-z]{2,}\b', text)
        tokens_ko = re.findall(r'[가-힣]+', text)
        
        stopwords = {'the', 'and', 'or', 'for', 'to', 'of', 'in', 'on', 'at', 'with', 'by', 'an', 'as', 'is', 'a',
                     '을', '를', '이', '가', '은', '는', '의', '에', '로', '함', '하기', '팀', '및'}
        
        all_tokens = set(tokens_en + tokens_ko)
        return set(t for t in all_tokens if t not in stopwords)

    def _compute_similarity(self, tokens1: set, tokens2: set) -> float:
        if not tokens1 or not tokens2:
            return 0.0
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        return intersection / union if union > 0 else 0.0

    def _suggest_duty_name(self, tasks: List[Dict]) -> str:
        # Check against pre-defined archetypes
        combined_text = " ".join([t['task_name'] for t in tasks]).lower()
        
        best_duty = "일반 관리 (General)"
        max_matches = 0
        
        for duty, keywords in self.duty_keywords.items():
            matches = sum(1 for k in keywords if k in combined_text)
            if matches > max_matches:
                max_matches = matches
                best_duty = duty
        
        if max_matches > 0:
            return best_duty
            
        # Fallback
        first_task = tasks[0]['task_name']
        return f"직무 그룹: {first_task} 등"

    def cluster_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clusters a list of raw tasks into 'Duties'.
        Input: [{'id': '..', 'task_name': '..', 'fte': 0.5}, ...]
        Output: [{'duty_name': '...', 'fte_sum': 1.2, 'tasks': [...]}, ...]
        """
        # 1. Incremental Clustering
        clusters = [] # List of list of tasks
        
        for task in tasks:
            task_tokens = self._tokenize(task['task_name'] + " " + task.get('action_verb', ''))
            
            best_cluster_idx = -1
            best_sim = 0.0
            
            for i, cluster in enumerate(clusters):
                # Compare with the 'centroid' (just the first task for simplicity in MVP)
                # Or compare with all? Let's compare with first task of cluster
                centroid_tokens = self._tokenize(cluster[0]['task_name'] + " " + cluster[0].get('action_verb', ''))
                sim = self._compute_similarity(task_tokens, centroid_tokens)
                if sim > best_sim:
                    best_sim = sim
                    best_cluster_idx = i
            
            # Threshold for Jaccard similarity
            if best_sim > 0.1: # Lower threshold for short text
                clusters[best_cluster_idx].append(task)
            else:
                clusters.append([task])

        # 2. Format Output & Post-Merge
        # Refine: If multiple clusters map to the same "Duty Name" (e.g. Tech Ops), merge them.
        duty_map = {} # duty_name -> {fte_sum, tasks}
        
        for cluster in clusters:
            duty_name = self._suggest_duty_name(cluster)
            fte_sum = sum(t.get('fte', 0) for t in cluster)
            
            if duty_name in duty_map:
                # Merge
                duty_map[duty_name]['tasks'].extend(cluster)
                duty_map[duty_name]['fte_sum'] += fte_sum
            else:
                # New entry
                duty_map[duty_name] = {
                    'duty_name': duty_name,
                    'fte_sum': fte_sum,
                    'tasks': cluster
                }
        
        results = []
        for d in duty_map.values():
            d['fte_sum'] = round(d['fte_sum'], 2)
            d['recommendation'] = self._generate_recommendation(d['duty_name'], d['fte_sum'])
            results.append(d)
            
        return results

    def _generate_recommendation(self, duty: str, fte: float) -> str:
        if fte > 1.2:
            if "행정" in duty or "Admin" in duty:
                return "과부하 경고 (Buy). 주니어 지원 인력 채용이 시급합니다."
            elif "전략" in duty or "Strategy" in duty:
                return "과부하 경고 (Build). 내부 인재를 육성하거나 권한을 위임하세요."
            elif "기술" in duty or "Tech" in duty:
                return "과부하 경고 (Buy). 전문 기술 인력 확충이 필요합니다."
            else:
                return "과부하 경고 (Red). 업무 재분배를 고려하세요."
        elif fte < 0.3:
            return "업무량 부족. 다른 역할과 통합을 고려하세요."
        else:
            return "적정 업무량 (Balanced)."
