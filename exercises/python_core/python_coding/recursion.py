import pandas as pd

def get_exercise():
    return {
        "title": "Recursion and Stack Limits",
        "subtitle": "recursion",
        "description": "Consider the following Python code snippet:\nBased on the code, which of the given statements is accurate regarding its performance?\n\n```python\ndef calculate_factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * calculate_factorial(n - 1)\n```",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "Unlike functional languages like Haskell or Elixir, Python does not natively optimize tail recursion. What happens to the C call stack if `n` is 10,000?",
        "solution_python": 'result = "The code has a high likelihood of encountering a stack overflow error for large input values of n."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

Recursion is an elegant mathematical concept, but in Python, it comes with a severe architectural limitation: **the call stack limit**.

Every time a function is called, Python allocates a new "stack frame" in memory. This frame holds the function's local variables, arguments, and the return address (where to go back to when the function finishes).
In our `calculate_factorial` function, the `return n * calculate_factorial(n - 1)` line forces Python to keep the current stack frame alive while waiting for the inner function call to finish.

If you call this with a large number (e.g., `calculate_factorial(5000)`), Python will attempt to create 5,000 stacked frames in memory simultaneously. Because CPython's execution stack is bounded to prevent unbounded memory consumption from crashing the host machine, Python artificially limits recursion (defaulting to 1000 frames). Exceeding this triggers a `RecursionError`.

Furthermore, Python **does not support Tail Call Optimization (TCO)**. Even if you wrote this algorithm in a tail-recursive manner, Python's creator deliberately decided against implementing TCO in order to preserve accurate, complete tracebacks for debugging.

- Option A is incorrect because iteration (loops) provides far more optimal performance for large numbers in Python.
- Option B is incorrect; Python does not implement tail recursion optimization.
- Option C is incorrect; the time complexity is O(N), not O(N^2).""",
        "big_o_explanation": "O(N) Time and O(N) Space - The algorithm must perform N multiplications and allocate N stack frames.",
        
        "mcq_questions": [
             {
                 "question": "Based on the factorial recursion code, which of the given statements is accurate regarding its performance?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "The code has optimal performance for calculating factorials of large numbers.", "is_correct": False},
                     {"label": "B", "text": "The code uses tail recursion and ensures optimal memory usage for calculating factorials.", "is_correct": False},
                     {"label": "C", "text": "The code has a time complexity of O(n^2) for calculating factorials.", "is_correct": False},
                     {"label": "D", "text": "The code has a high likelihood of encountering a stack overflow error for large input values of n.", "is_correct": True},
                 ],
                 "explanation": "Python has a built-in recursion limit to prevent infinite loops from crashing the C stack. Because Python does not optimize for tail recursion, calculating the factorial of a large number will exhaust the call stack, raising a RecursionError."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Recursion and Stack Limits",
                "scenario": "Consider the following Python code snippet:\nBased on the code, which of the given statements is accurate regarding its performance?\n\n```python\ndef calculate_factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * calculate_factorial(n - 1)\n```",
                "hint": "Unlike functional languages like Haskell or Elixir, Python does not natively optimize tail recursion. What happens to the C call stack if `n` is 10,000?",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of recursion limits in Python", "Knowledge of stack frame allocation and lack of tail-call optimization"],
                "solution_code": 'result = "The code has a high likelihood of encountering a stack overflow error for large input values of n."',
                "expected_output": 'The code has a high likelihood of encountering a stack overflow error for large input values of n.',
                "big_o_explanation": "O(N) Time and O(N) Space - The algorithm must perform N multiplications and allocate N stack frames.",
                "follow_up_probes": ["How would you rewrite this to be iterative?", "How can you manually change the recursion limit in Python?"]
            }
        ]
    }
