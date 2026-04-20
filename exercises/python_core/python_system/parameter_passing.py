import pandas as pd

def get_exercise():
    return {
        "title": "Parameter Passing",
        "subtitle": "Core python concepts",
        "description": """How are arguments passed to functions in Python?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": "No specific code setup required for this conceptual problem.",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = True # Concept exercise placeholder',
        "deep_dive": """In Python, everything is an object. When passing arguments, the local variable receives a copy of the reference to the original object. Mutable objects modified in-place affect the caller, while reassignments or modifications to immutable objects create new objects locally.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """How are arguments passed to functions in Python?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """Always by value; a copy of the argument is passed, and the original is never modified.""", "is_correct": False},
                     {"label": "B", "text": """Always by reference; a pointer to the original argument is passed and can always be changed.""", "is_correct": False},
                     {"label": "C", "text": """By \"pass-by-assignment,\" where the function gets a copy of the reference to the object.""", "is_correct": True},
                     {"label": "D", "text": """Primitive types are passed by value, while all objects are passed by reference.""", "is_correct": False},
                 ],
                 "explanation": """In Python, everything is an object. When passing arguments, the local variable receives a copy of the reference to the original object. Mutable objects modified in-place affect the caller, while reassignments or modifications to immutable objects create new objects locally."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """How are arguments passed to functions in Python?

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
