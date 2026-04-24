import pandas as pd

def get_exercise():
    return {
        "title": "Recursion Depth Limits",
        "subtitle": "recursion",
        "description": "Consider the following Python code snippet:\n\nBased on the code, which of the given statements is accurate regarding its performance?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """\
def calculate_factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * calculate_factorial(n - 1)""",
        "allowed_modes": ["Python"],
        "hint_python": "Consider how Python handles the call stack and whether it supports Tail Call Optimization.",
        "solution_python": 'result = "The code has a high likelihood of encountering a stack overflow error for large input values of n."',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis question evaluates your understanding of Python's recursion limits and stack management.\n\n* **No Tail Call Optimization (TCO):** Unlike some functional languages, Python does not natively optimize tail-recursive calls. Each recursive call adds a new frame to the call stack.\n* **Recursion Limit:** Python has a strict default recursion depth limit (typically 1000). If you attempt to calculate `calculate_factorial(2000)`, the stack will overflow before reaching the base case, raising a `RecursionError`.\n\nFor large-scale processing, an iterative approach or techniques like trampolining are required in Python to bypass these constraints.",
        "big_o_explanation": "O(n) - The time and space complexity are both O(n), where n is the input number, because each step requires an additional stack frame.",

        # --- MULTICHOICE CONCEPTUAL QUESTIONS ---
        "mcq_questions": [
             {
                 "question": "Based on the code, which of the given statements is accurate regarding its performance?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "The code has optimal performance for calculating factorials of large numbers.", "is_correct": False},
                     {"label": "B", "text": "The code uses tail recursion and ensures optimal memory usage for calculating factorials.", "is_correct": False},
                     {"label": "C", "text": "The code has a time complexity of O(n^2) for calculating factorials.", "is_correct": False},
                     {"label": "D", "text": "The code has a high likelihood of encountering a stack overflow error for large input values of n.", "is_correct": True},
                 ],
                 "explanation": "Python has a strict recursion depth limit (usually 1000) and does not support Tail Call Optimization (TCO). Calling this function with a large n will cause a RecursionError before completing."
             }
        ],

        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "Consider the following Python code snippet:\n\nBased on the code, which of the given statements is accurate regarding its performance?",
                "hint": "Consider how Python handles the call stack and whether it supports Tail Call Optimization.",
                "data": """\
def calculate_factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * calculate_factorial(n - 1)""",
                "evaluation_criteria": ["Understanding of RecursionError", "Knowledge of Python's lack of TCO"],
                "solution_code": 'result = "The code has a high likelihood of encountering a stack overflow error for large input values of n."',
                "expected_output": 'The code has a high likelihood of encountering a stack overflow error for large input values of n.',
                "big_o_explanation": "O(n) Space - A new stack frame is created for each call up to n.",
                "follow_up_probes": ["How would you rewrite this function to prevent a RecursionError?"]
            }
        ]
    }
