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
        "solution_python": 'result = "Execution continues"',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**
This question evaluates your understanding of the Context Manager protocol (`__enter__` and `__exit__`), which is fundamental for writing robust, resource-safe Python code. 

Here is the exact execution flow at the interpreter level:
1. **The Exception:** Inside the `with` block, `int("Not a number")` throws a `ValueError`.
2. **The Hand-off:** Python immediately halts the block and passes the exception details (`exc_type`, `exc_value`, `traceback`) into the context manager's `__exit__` method.
3. **The Interception:** Inside `__exit__`, the code checks `if exc_type is ValueError:`. This evaluates to True. It prints the suppression message and, crucially, **returns `True`**.
4. **The Suppression:** In Python's Context Manager protocol, if the `__exit__` method returns `True`, it acts as a signal to the interpreter: *"I have successfully handled this exception, do not propagate it further."* Python gracefully suppresses the crash.
5. **Resumption:** Execution resumes immediately *after* the `with` block, hitting the final `print("Execution continues")` statement.

As a lead, leveraging custom context managers is the cleanest way to abstract away repetitive setup/teardown logic (like database transactions, lock acquisition, or API session handling).""",
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
                "hint": "Look at the return value of the __exit__ method. How does Python handle exceptions inside a 'with' block based on that boolean?",
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
                "evaluation_criteria": ["Mastery of the Context Manager Protocol", "Understanding of exception propagation and suppression", "Clean code practices"],
                "solution_code": 'result = "Execution continues"',
                "expected_output": "Execution continues",
                "big_o_explanation": "O(1) Time/Space overhead for the context management block.",
                "follow_up_probes": ["How would you write this exact same context manager using the @contextlib.contextmanager decorator?", "What happens if __exit__ returns None instead of False?"]
            }
        ]
    }
