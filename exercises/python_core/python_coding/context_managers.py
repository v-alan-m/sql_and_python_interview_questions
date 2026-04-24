import pandas as pd

def get_exercise():
    return {
        "title": "Context Managers and Exception Suppression",
        "subtitle": "context-managers",
        "description": "Analyze the custom context manager below:\n\n```python\nclass SuppressError:\n    def __enter__(self):\n        return self\n    def __exit__(self, exc_type, exc_value, traceback):\n        if exc_type is ValueError:\n            print(\"ValueError suppressed\")\n            return True\n        return False\n\nwith SuppressError():\n    int(\"Not a number\")\nprint(\"Execution continues\")\n```\n\nWhat is the console output when this script runs?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "Look at what the `__exit__` method returns when a `ValueError` is encountered. How does Python interpret a `True` return value from `__exit__`?",
        "solution_python": 'result = "ValueError suppressed\\nExecution continues"',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

Context managers are predominantly used for resource management (like acquiring/releasing locks or opening/closing files) via the `with` statement. The protocol consists of `__enter__` and `__exit__` methods.

A lesser-known, yet incredibly powerful feature of context managers is their ability to act as selective exception handlers. When an exception is raised inside the `with` block, Python immediately pauses execution and calls the `__exit__` method, passing the exception type, value, and traceback as arguments.

The return value of `__exit__` dictates what happens next:
1. If `__exit__` returns `False` (or `None`, which is implicitly false), Python assumes the exception was not handled and propagates it upward.
2. If `__exit__` returns `True`, Python assumes the exception was intentionally swallowed and fully resolved. It suppresses the exception entirely, and execution resumes normally on the next line immediately *after* the `with` block.

In this code, `int("Not a number")` throws a `ValueError`. The `__exit__` method catches it, prints `"ValueError suppressed"`, and returns `True`. Because it returns `True`, the program does not crash, and the subsequent `print("Execution continues")` executes flawlessly.

- Option A is incorrect because the return `True` intercepts and suppresses the traceback.
- Option C is incorrect because it misses the `print` statement inside the `__exit__` block.
- Option D is incorrect because returning `None` is standard behavior (which propagates exceptions), it does not trigger a `TypeError`.""",
        "big_o_explanation": "O(1) - Context manager setup and teardown are constant-time operations.",
        
        "mcq_questions": [
             {
                 "question": "What is the console output when the provided custom context manager script runs?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "A standard ValueError traceback crashing the program.", "is_correct": False},
                     {"label": "B", "text": "ValueError suppressed\nExecution continues", "is_correct": True},
                     {"label": "C", "text": "Execution continues", "is_correct": False},
                     {"label": "D", "text": "A TypeError, because __exit__ does not return None.", "is_correct": False},
                 ],
                 "explanation": "When an exception occurs inside a 'with' block, Python passes the exception details to the context manager's __exit__ method. If __exit__ returns True, Python gracefully suppresses the exception and execution resumes immediately after the 'with' block. Since int(\"Not a number\") raises a ValueError, our __exit__ method returns True, avoiding the crash and printing both statements."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Context Managers and Exception Suppression",
                "scenario": "Analyze the custom context manager below:\n\n```python\nclass SuppressError:\n    def __enter__(self):\n        return self\n    def __exit__(self, exc_type, exc_value, traceback):\n        if exc_type is ValueError:\n            print(\"ValueError suppressed\")\n            return True\n        return False\n\nwith SuppressError():\n    int(\"Not a number\")\nprint(\"Execution continues\")\n```\n\nWhat is the console output when this script runs?",
                "hint": "Look at what the `__exit__` method returns when a `ValueError` is encountered. How does Python interpret a `True` return value from `__exit__`?",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of the context management protocol (__enter__, __exit__)", "Knowledge of exception suppression mechanics using return values in __exit__"],
                "solution_code": 'result = "ValueError suppressed\\nExecution continues"',
                "expected_output": 'ValueError suppressed\nExecution continues',
                "big_o_explanation": "O(1) - Context manager setup and teardown are constant-time operations.",
                "follow_up_probes": ["What happens if `int()` did not raise an exception? What would `exc_type` evaluate to?", "How does `contextlib.suppress` work under the hood?"]
            }
        ]
    }
