import pandas as pd

def get_exercise():
    return {
        "title": "Garbage Collection",
        "subtitle": "Core python concepts",
        "description": """In Python, standard memory management relies heavily on reference counting. However, which of the following scenarios specifically requires Python's generational cyclic garbage collector to intervene to prevent memory leaks?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": "No specific code setup required for this conceptual problem.",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = True # Concept exercise placeholder',
        "deep_dive": """Reference counting immediately deallocates an object when its count hits zero. However, if object A references object B, and B references A, their internal reference counts remain at least 1 even if all external variables pointing to them are deleted. The cyclic garbage collector periodically sweeps for these unreachable \"islands\" of memory to reclaim them.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """In Python, standard memory management relies heavily on reference counting. However, which of the following scenarios specifically requires Python's generational cyclic garbage collector to intervene to prevent memory leaks?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """A large list of immutable integers being repeatedly overwritten.""", "is_correct": False},
                     {"label": "B", "text": """Two custom object instances that maintain attributes pointing to each other, creating an isolated island after their original variables are deleted.""", "is_correct": True},
                     {"label": "C", "text": """Deeply nested recursive function calls that exceed the recursion depth limit.""", "is_correct": False},
                     {"label": "D", "text": """Opening a file connection without using a context manager or explicitly calling close().""", "is_correct": False},
                 ],
                 "explanation": """Reference counting immediately deallocates an object when its count hits zero. However, if object A references object B, and B references A, their internal reference counts remain at least 1 even if all external variables pointing to them are deleted. The cyclic garbage collector periodically sweeps for these unreachable \"islands\" of memory to reclaim them."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """In Python, standard memory management relies heavily on reference counting. However, which of the following scenarios specifically requires Python's generational cyclic garbage collector to intervene to prevent memory leaks?

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
