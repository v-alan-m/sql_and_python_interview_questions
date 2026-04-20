import pandas as pd

def get_exercise():
    return {
        "title": "Data Structures",
        "subtitle": "Core python concepts",
        "description": """What is the primary performance benefit of using a set instead of a list to check for the existence of an item?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": "No specific code setup required for this conceptual problem.",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = True # Concept exercise placeholder',
        "deep_dive": """Sets are implemented using hash tables, allowing Python to calculate a hash and immediately jump to the memory bucket for an average O(1) constant time lookup. Lists require an O(n) linear scan on average. Sets actually consume more memory than lists due to hash table overhead.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """What is the primary performance benefit of using a set instead of a list to check for the existence of an item?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """Sets consume significantly less memory for the same number of elements.""", "is_correct": False},
                     {"label": "B", "text": """Sets use hash tables, providing average O(1) time for membership testing.""", "is_correct": True},
                     {"label": "C", "text": """Sets maintain their elements in a sorted order, which allows for faster binary searching.""", "is_correct": False},
                     {"label": "D", "text": """Lists require a linear scan, which has a best-case time complexity of O(n).""", "is_correct": False},
                 ],
                 "explanation": """Sets are implemented using hash tables, allowing Python to calculate a hash and immediately jump to the memory bucket for an average O(1) constant time lookup. Lists require an O(n) linear scan on average. Sets actually consume more memory than lists due to hash table overhead."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """What is the primary performance benefit of using a set instead of a list to check for the existence of an item?

""",
                "hint": "Return True to pass the concept check.",
                "data": "No specific code setup required for this conceptual problem.",
                "evaluation_criteria": ["Understanding of concept"],
                "solution_code": """\
result = True""",
                "expected_output": True,
                "big_o_explanation": "Constant time implementation.",
                "follow_up_probes": ["Can you explain the limitations?"]
            }
        ]
    }
