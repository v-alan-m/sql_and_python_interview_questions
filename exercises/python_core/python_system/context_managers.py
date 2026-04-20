import pandas as pd

def get_exercise():
    return {
        "title": "Context Managers",
        "subtitle": "Core python concepts",
        "description": """Analyze the custom context manager below:\n\nWhat is the console output when this script runs?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """\
class SuppressError:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is ValueError:
            print(\"ValueError suppressed\")
            return True
        return False

with SuppressError():
    int(\"Not a number\")
print(\"Execution continues\")""",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = True # Concept exercise placeholder',
        "deep_dive": """When an exception occurs inside a 'with' block, Python passes the exception details to the context manager's __exit__ method. If __exit__ returns True, Python gracefully suppresses the exception and execution resumes immediately after the 'with' block. Since int(\"Not a number\") raises a ValueError, our __exit__ method returns True, avoiding the crash and printing both statements.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """Analyze the custom context manager below:\n\nWhat is the console output when this script runs?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """A standard ValueError traceback crashing the program.""", "is_correct": False},
                     {"label": "B", "text": """ValueError suppressedExecution continues""", "is_correct": False},
                     {"label": "C", "text": """Execution continues""", "is_correct": True},
                     {"label": "D", "text": """A TypeError, because __exit__ does not return None.""", "is_correct": False},
                 ],
                 "explanation": """When an exception occurs inside a 'with' block, Python passes the exception details to the context manager's __exit__ method. If __exit__ returns True, Python gracefully suppresses the exception and execution resumes immediately after the 'with' block. Since int(\"Not a number\") raises a ValueError, our __exit__ method returns True, avoiding the crash and printing both statements."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """Analyze the custom context manager below:

What is the console output when this script runs?

""",
                "hint": "Return True to pass the concept check.",
                "data": """\
class SuppressError:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is ValueError:
            print(\"ValueError suppressed\")
            return True
        return False

with SuppressError():
    int(\"Not a number\")
print(\"Execution continues\")""",
                "evaluation_criteria": ["Understanding of concept"],
                "solution_code": """\
result = True""",
                "expected_output": True,
                "big_o_explanation": "Constant time implementation.",
                "follow_up_probes": ["Can you explain the limitations?"]
            }
        ]
    }
