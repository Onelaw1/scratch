from typing import List, Dict
import random

class TemplateJDGenerator:
    def __init__(self):
        # "Verb Expander" Dictionary
        self.verb_map = {
            "manage": [
                "Oversee and manage the execution of",
                "Lead and direct the operations of",
                "Strategically manage and optimize"
            ],
            "analyze": [
                "Conduct in-depth analysis of",
                "Analyze complex data sets to drive insights regarding",
                "Evaluate and interpret key metrics related to"
            ],
            "develop": [
                "Design, develop, and implement",
                "Innovate and create robust solutions for",
                "Spearhead the development of"
            ],
            "support": [
                "Provide comprehensive support for",
                "Actively assist and facilitate",
                "Partner with stakeholders to support"
            ]
        }
        
        self.grade_qualifications = {
            "G1": "Bachelor's degree and 0-2 years of relevant experience.",
            "G2": "Bachelor's degree and 3-5 years of experience. Demonstrated ability to work independently.",
            "G3": "Master's degree preferred. 5-8 years of experience with proven track record of project management.",
            "G4": "Advanced degree required. 8-12 years of leadership experience in a related field.",
            "G5": "Executive level experience (15+ years). Proven strategic vision and industry expertise."
        }

    def _expand_task(self, task_name: str, action_verb: str) -> str:
        """Expands a simple task into a professional responsibility bullet."""
        verb_key = action_verb.lower().strip()
        
        # Try to match the exact verb, or find a key that is contained in the verb
        found_key = None
        if verb_key in self.verb_map:
            found_key = verb_key
        else:
            for k in self.verb_map:
                if k in verb_key:
                    found_key = k
                    break
        
        prefix = ""
        if found_key:
            prefix = random.choice(self.verb_map[found_key])
            # If the task name starts with the verb, remove it to avoid repetition
            # e.g. Task: "Manage Team", Verb: "Manage" -> Prefix: "Oversee..." -> Result: "Oversee... Team"
            clean_task = task_name 
            if clean_task.lower().startswith(action_verb.lower()):
                 clean_task = clean_task[len(action_verb):].strip()
            
            return f"{prefix} {clean_task} to ensure organizational excellence."
        else:
            # Fallback
            return f"{action_verb.capitalize()} {task_name} effectively."

    def generate(self, position_title: str, position_grade: str, tasks: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Generates a Job Description draft.
        tasks: List of dicts with 'task_name' and 'action_verb'
        """
        
        # 1. Overview
        overview = (
            f"We are seeking a highly motivated and skilled {position_title} "
            f"to join our team. This {position_grade} level role plays a critical part in "
            f"driving our mission forward. The ideal candidate will have strong expertise "
            f"in {tasks[0]['task_name'] if tasks else 'related fields'} and a passion for excellence."
        )

        # 2. Responsibilities
        bullets = []
        for t in tasks:
            bullet = self._expand_task(t.get('task_name', ''), t.get('action_verb', ''))
            bullets.append(f"• {bullet}")
        
        responsibilities = "\n".join(bullets)

        # 3. Qualifications
        qualifications = self.grade_qualifications.get(position_grade, "Relevant degree and experience required.")
        qualifications += "\n• Strong communication and interpersonal skills.\n• Ability to work collaboratively in a fast-paced environment."

        return {
            "title": position_title,
            "grade": position_grade,
            "overview": overview,
            "responsibilities": responsibilities,
            "qualifications": qualifications
        }
