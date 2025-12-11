import os
import json
import sqlite3
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class KnowledgeNode(BaseModel):
    category: str  # e.g., "Client_Preference", "Framework", "Past_Success"
    key: str       # e.g., "Public_Sector_Tone", "SWOT_Analysis"
    value: str     # The actual content
    tags: List[str] = []

class MemoryService:
    def __init__(self, db_path: str = "c:/Users/Administrator/Downloads/Root/Job_Management_System/sql_app.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the memory table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def add_memory(self, node: KnowledgeNode):
        """Add a new piece of knowledge to long-term memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO agent_memory (category, key, value, tags) VALUES (?, ?, ?, ?)",
            (node.category, node.key, node.value, json.dumps(node.tags))
        )
        conn.commit()
        conn.close()
        print(f"Memory Added: [{node.category}] {node.key}")

    def retrieve_context(self, query: str) -> str:
        """
        Retrieve relevant context based on a query.
        For now, this uses simple keyword matching. 
        In the future, this can be upgraded to vector search (RAG).
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Simple heuristic: fetch all 'Client_Preference' and 'Persona'
        # In a real system, we would embed the query and search.
        cursor.execute("SELECT * FROM agent_memory WHERE category IN ('Client_Preference', 'Persona', 'Framework')")
        rows = cursor.fetchall()
        conn.close()

        context_parts = []
        for row in rows:
            # Simple keyword filtering
            if any(word.lower() in query.lower() for word in row['tags'].lower().split(',')) or row['category'] == 'Persona':
                context_parts.append(f"- [{row['category']}] {row['key']}: {row['value']}")
        
        if not context_parts:
            return "No specific past context found."
            
        return "\n".join(context_parts)

    def seed_initial_persona(self):
        """Seed the DB with the user's specific persona."""
        persona_data = [
            KnowledgeNode(
                category="Persona",
                key="Role",
                value="CEO & Principal Consultant (MBB Alum + Public Sector Expert). Target Audience: Evaluation Committee (Professors).",
                tags=["identity", "role", "evaluator_focus"]
            ),
            KnowledgeNode(
                category="Client_Preference",
                key="Core_Values",
                value="Evidence-Based, Academic Rigor, Compliance with Evaluation Manual, Public Value.",
                tags=["evidence", "rigor", "compliance"]
            ),
            KnowledgeNode(
                category="Client_Preference",
                key="Tone",
                value="Dry, objective, authoritative (Professor-to-Professor). No fluff.",
                tags=["tone", "style", "academic"]
            )
        ]
        
        for node in persona_data:
            # Check if exists to avoid duplicates on restart
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM agent_memory WHERE key = ?", (node.key,))
            if not cursor.fetchone():
                self.add_memory(node)
            conn.close()

if __name__ == "__main__":
    # Test
    memory = MemoryService()
    memory.seed_initial_persona()
    print(memory.retrieve_context("Create a strategy for a public institution"))
