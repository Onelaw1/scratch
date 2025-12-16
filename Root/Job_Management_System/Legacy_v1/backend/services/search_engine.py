import math
import re
from collections import defaultdict
from typing import List, Dict, Tuple

class TFIDFEngine:
    def __init__(self):
        self.documents: Dict[str, str] = {}  # id -> text
        self.index: Dict[str, List[str]] = defaultdict(list) # term -> [doc_ids]
        self.idf: Dict[str, float] = {}
        self.doc_vectors: Dict[str, Dict[str, float]] = {}
        
    def _tokenize(self, text: str) -> List[str]:
        # Simple regex tokenizer: lowercase, remove non-alphanumeric
        text = text.lower()
        tokens = re.findall(r'\b[a-z]{2,}\b', text)
        # minimal stopword list
        stopwords = {'the', 'and', 'or', 'for', 'to', 'of', 'in', 'on', 'at', 'with', 'by', 'an', 'as', 'is'}
        return [t for t in tokens if t not in stopwords]

    def add_document(self, doc_id: str, text: str):
        self.documents[doc_id] = text
        tokens = self._tokenize(text)
        
        # Calculate Term Frequency (TF) for this doc
        tf = defaultdict(int)
        for t in tokens:
            tf[t] += 1
            
        # Store raw TF for now, will compute TF-IDF on build
        self.doc_vectors[doc_id] = {t: count/len(tokens) for t, count in tf.items()}
        
    def build_index(self):
        # Calculate IDF
        N = len(self.documents)
        doc_counts = defaultdict(int)
        
        for doc_id, vec in self.doc_vectors.items():
            for term in vec.keys():
                doc_counts[term] += 1
                
        self.idf = {term: math.log(N / (count)) for term, count in doc_counts.items()}
        
        # Finalize Doc Vectors (TF * IDF)
        for doc_id, vec in self.doc_vectors.items():
            for term, tf_val in vec.items():
                self.doc_vectors[doc_id][term] = tf_val * self.idf.get(term, 0)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
            
        # Query Vector (TF only is usually enough for query, but let's use IDF too)
        query_vec = defaultdict(float)
        for t in query_tokens:
            query_vec[t] += 1
        
        # Normalize Query Vector
        total = sum(query_vec.values())
        query_vec = {t: (c/total) * self.idf.get(t, 0) for t, c in query_vec.items()}
        
        # Cosine Similarity
        scores = defaultdict(float)
        query_norm = math.sqrt(sum(v**2 for v in query_vec.values()))
        
        if query_norm == 0:
            return []

        # Find candidate docs (any doc containing query terms)
        candidate_docs = set()
        for t in query_vec.keys():
            # In a real inverted index we'd look up docs here. 
            # Since we iterate all docs for simplicity in this MVP:
            pass 

        for doc_id, doc_vec in self.doc_vectors.items():
            dot_product = 0
            doc_norm = math.sqrt(sum(v**2 for v in doc_vec.values()))
            
            common_terms = set(query_vec.keys()) & set(doc_vec.keys())
            for term in common_terms:
                dot_product += query_vec[term] * doc_vec[term]
                
            if doc_norm > 0:
                scores[doc_id] = dot_product / (query_norm * doc_norm)
                
        # Sort and return top K
        results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return results[:top_k]
