import pandas as pd

def get_exercise():
    return {
        "title": "Built Ins",
        "subtitle": "Core python concepts",
        "description": """What does the following print function call output to the console?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """\
print('python', 'is', 'fun', sep='-', end='!')""",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = True # Concept exercise placeholder',
        "deep_dive": """The print() function joins positional string arguments using the string provided to the sep keyword argument (a hyphen). It ends the output with the string provided to the end keyword argument (an exclamation mark) instead of the default newline.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """What does the following print function call output to the console?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """python-is-fun!""", "is_correct": True},
                     {"label": "B", "text": """python is fun!""", "is_correct": False},
                     {"label": "C", "text": """python, is, fun!""", "is_correct": False},
                     {"label": "D", "text": """python-is-fun !""", "is_correct": True},
                 ],
                 "explanation": """The print() function joins positional string arguments using the string provided to the sep keyword argument (a hyphen). It ends the output with the string provided to the end keyword argument (an exclamation mark) instead of the default newline."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """What does the following print function call output to the console?

""",
                "hint": "Return True to pass the concept check.",
                "data": """\
print('python', 'is', 'fun', sep='-', end='!')""",
                "evaluation_criteria": ["Understanding of concept"],
                "solution_code": """\
result = True""",
                "expected_output": True,
                "big_o_explanation": "Constant time implementation.",
                "follow_up_probes": ["Can you explain the limitations?"]
            }
        ]
    }
