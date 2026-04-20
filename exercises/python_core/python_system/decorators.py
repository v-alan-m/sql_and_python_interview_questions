import pandas as pd

def get_exercise():
    return {
        "title": "Decorators",
        "subtitle": "Core python concepts",
        "description": """You are writing a logging decorator for a framework, but users complain that their function docstrings and names are disappearing. Look at the code:\n\nWhat does the print statement currently output, and how do you fix it at the system level?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """\
import functools

def log_call(func):
    def wrapper(*args, **kwargs):
        \"\"\"Wrapper docstring\"\"\"
        print(f\"Calling {func.__name__}\")
        return func(*args, **kwargs)
    return wrapper

@log_call
def calculate_tax(amount):
    \"\"\"Calculates standard tax.\"\"\"
    return amount * 0.2

print(calculate_tax.__name__)""",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = True # Concept exercise placeholder',
        "deep_dive": """A decorator essentially replaces the original function with the wrapper function. Without @functools.wraps, introspection tools (like help() or __name__) will only see the name 'wrapper' and its 'Wrapper docstring'. The @wraps decorator safely copies crucial metadata (__module__, __name__, __qualname__, __doc__) from the original function to the new wrapper.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """You are writing a logging decorator for a framework, but users complain that their function docstrings and names are disappearing. Look at the code:\n\nWhat does the print statement currently output, and how do you fix it at the system level?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """Output: calculate_tax. Fix: No fix needed.""", "is_correct": False},
                     {"label": "B", "text": """Output: wrapper. Fix: Add @functools.wraps(func) directly above the 'def wrapper' definition to copy the original function's metadata.""", "is_correct": True},
                     {"label": "C", "text": """Output: log_call. Fix: Add wrapper.__name__ = func.__name__ inside the wrapper function body.""", "is_correct": False},
                     {"label": "D", "text": """Output: wrapper. Fix: Pass the calculate_tax function as an explicit string to the decorator.""", "is_correct": False},
                 ],
                 "explanation": """A decorator essentially replaces the original function with the wrapper function. Without @functools.wraps, introspection tools (like help() or __name__) will only see the name 'wrapper' and its 'Wrapper docstring'. The @wraps decorator safely copies crucial metadata (__module__, __name__, __qualname__, __doc__) from the original function to the new wrapper."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """You are writing a logging decorator for a framework, but users complain that their function docstrings and names are disappearing. Look at the code:

What does the print statement currently output, and how do you fix it at the system level?

""",
                "hint": "Return True to pass the concept check.",
                "data": """\
import functools

def log_call(func):
    def wrapper(*args, **kwargs):
        \"\"\"Wrapper docstring\"\"\"
        print(f\"Calling {func.__name__}\")
        return func(*args, **kwargs)
    return wrapper

@log_call
def calculate_tax(amount):
    \"\"\"Calculates standard tax.\"\"\"
    return amount * 0.2

print(calculate_tax.__name__)""",
                "evaluation_criteria": ["Understanding of concept"],
                "solution_code": """\
result = True""",
                "expected_output": True,
                "big_o_explanation": "Constant time implementation.",
                "follow_up_probes": ["Can you explain the limitations?"]
            }
        ]
    }
