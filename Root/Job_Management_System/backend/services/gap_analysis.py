from typing import List, Dict, Any
from collections import defaultdict
import math
import re

class SmartWorkloadAnalyzer:
    def __init__(self):
        # Pre-defined duty archetypes for "Auto-Labeling" clusters
        self.duty_keywords = {
            "Administrative Support": ["email", "schedule", "meeting", "filing", "admin", "calendar", "call"],
            "Strategic Planning": ["strategy", "plan", "vision", "roadmap", "lead", "goal", "budget"],
            "Technical Operations": ["code", "develop", "system", "server", "analysis", "data", "fix", "bug"],
            "Client Services": ["client", "customer", "support", "ticket", "service", "complaint"]
        }

    def _tokenize(self, text: str) -> set:
        text = text.lower()
        tokens = re.findall(r'\b[a-z]{2,}\b', text)
        stopwords = {'the', 'and', 'or', 'for', 'to', 'of', 'in', 'on', 'at', 'with', 'by', 'an', 'as', 'is', 'a'}
        return set(t for t in tokens if t not in stopwords)

    def _compute_similarity(self, tokens1: set, tokens2: set) -> float:
        if not tokens1 or not tokens2:
            return 0.0
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        return intersection / union if union > 0 else 0.0

    def _suggest_duty_name(self, tasks: List[Dict]) -> str:
        # Check against pre-defined archetypes
        combined_text = " ".join([t['task_name'] for t in tasks]).lower()
        
        best_duty = "General Duties"
        max_matches = 0
        
        for duty, keywords in self.duty_keywords.items():
            matches = sum(1 for k in keywords if k in combined_text)
            if matches > max_matches:
                max_matches = matches
                best_duty = duty
        
        if max_matches > 0:
            return best_duty
            
        # If no archetype matches, use the most frequent bigram or word?
        # For MVP, just return "Specialized Duty A/B/C" or the first task name
        return f"Duty: {tasks[0]['task_name']} et al."

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
            if best_sim > 0.3: 
                clusters[best_cluster_idx].append(task)
            else:
                clusters.append([task])

        # 2. Format Output
        results = []
        for cluster in clusters:
            fte_sum = sum(t.get('fte', 0) for t in cluster)
            duty_name = self._suggest_duty_name(cluster)
            
            results.append({
                "duty_name": duty_name,
                "fte_sum": round(fte_sum, 2),
                "tasks": cluster,
                "recommendation": self._generate_recommendation(duty_name, fte_sum)
            })
            
        return results

    def _generate_recommendation(self, duty: str, fte: float) -> str:
        if fte > 1.2:
            if "Admin" in duty:
                return "Critical Overload (Buy). Hire junior support staff."
            elif "Strategy" in duty:
                return "Critical Overload (Build). Promote internal talent or delegate."
            else:
                return "High Workload. Consider redistributing tasks."
        elif fte < 0.3:
            return "Underutilized. Consider combining with other roles."
        else:
            return "Balanced Workload."
