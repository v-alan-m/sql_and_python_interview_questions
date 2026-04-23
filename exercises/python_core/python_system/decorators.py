import pandas as pd

def get_exercise():
    return {
        "title": "Decorators",
        "subtitle": "Decorators",
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
        "solution_python": """result = "Output: wrapper. Fix: Add @functools.wraps(func) directly above the 'def wrapper' definition to copy the original function's metadata." """,
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**
This question tests your mastery of the Decorator design pattern and Python introspection. When building SDKs or frameworks, decorators are essential, but poorly written ones destroy developer experience by obfuscating debugging information.

Here is why this happens and how to fix it:
1. **The Replacement:** A decorator like `@log_call` essentially executes `calculate_tax = log_call(calculate_tax)`. The original `calculate_tax` function is completely replaced by the `wrapper` function returned by the decorator.
2. **Lost Metadata:** Because the variable now points to the `wrapper` function, any introspection tool (like calling `help()`, checking `__name__`, or reading stack traces) will see the name "wrapper" and the "Wrapper docstring". The original function's identity is lost.
3. **The Solution:** The standard library provides `functools.wraps`. By applying `@wraps(func)` to your inner wrapper function, Python safely copies crucial metadata (`__module__`, `__name__`, `__qualname__`, `__doc__`, and type annotations) from the original function over to the wrapper. 

Always mandate the use of `functools.wraps` in code reviews to ensure logs, stack traces, and IDE tooltips remain accurate and developer-friendly.""",
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
                "hint": "When a decorator wraps a function, what happens to the original function's name and docstring unless explicitly preserved?",
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
                "evaluation_criteria": ["Understanding of the Decorator pattern", "Fluency with functools and introspection", "Commitment to Developer Experience (DX)"],
                "solution_code": """result = "Output: wrapper. Fix: Add @functools.wraps(func) directly above the 'def wrapper' definition to copy the original function's metadata." """,
                "expected_output": "Output: wrapper. Fix: Add @functools.wraps(func) directly above the 'def wrapper' definition to copy the original function's metadata.",
                "big_o_explanation": "O(1) Time/Space overhead. The decorator simply adds a thin execution wrapper.",
                "follow_up_probes": ["How would you write a decorator that accepts its own arguments (e.g., @log_call(level='DEBUG'))?", "How do decorators interact with class methods vs static methods?"]
            }
        ]
    }
