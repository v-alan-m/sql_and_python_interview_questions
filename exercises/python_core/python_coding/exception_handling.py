import pandas as pd

def get_exercise():
    return {
        "title": "Exception Handling and the Finally Block",
        "subtitle": "exception-handling",
        "description": "What will be the output of the following function call?\n\n```python\ndef fetch_data():\n    try:\n        return \"Try Block\"\n    except Exception:\n        return \"Except Block\"\n    finally:\n        return \"Finally Block\"\n\nprint(fetch_data())\n```",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "Consider the execution guarantee of the `finally` block. If `finally` contains a return statement, how does it interact with return statements triggered earlier in the `try` block?",
        "solution_python": 'result = "Finally Block"',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

The `try/except/finally` construct is the backbone of robust error handling and resource cleanup in Python. The core contract of the `finally` block is that it is **guaranteed to execute**, regardless of whether an exception was raised, caught, or completely avoided.

However, a critical edge case arises when `return`, `break`, or `continue` statements are placed directly inside the `finally` block.
When Python executes the `try` block and encounters `return "Try Block"`, it evaluates the return value and prepares to exit the function. But before it can actually hand control back to the caller, it realizes there is a `finally` block pending.

Execution jumps to the `finally` block. Inside `finally`, Python encounters another `return` statement: `return "Finally Block"`. Because the `finally` block represents the absolute last step of the function's lifecycle, its control-flow statements take strict precedence. The original pending return value (`"Try Block"`) is permanently discarded and overwritten by `"Finally Block"`.

As a lead engineer, you should **never** place `return` statements inside a `finally` block in production code. It silently swallows exceptions (even if an error occurred in the `try` block, returning from `finally` cancels the exception propagation) and leads to incredibly confusing bugs where expected return values mysteriously disappear.

- Option A is incorrect because the `finally` block intercepts and overrides the `try` block's return.
- Option B is incorrect because no exception was raised to trigger the `except` block.
- Option D is incorrect; the syntax is perfectly valid Python.""",
        "big_o_explanation": "O(1) - Exception handling and block transitions operate in constant time.",
        
        "mcq_questions": [
             {
                 "question": "What will be the output of the provided function call containing a return statement inside the finally block?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "Try Block", "is_correct": False},
                     {"label": "B", "text": "Except Block", "is_correct": False},
                     {"label": "C", "text": "Finally Block", "is_correct": True},
                     {"label": "D", "text": "A SyntaxError is raised.", "is_correct": False},
                 ],
                 "explanation": "The finally block is guaranteed to execute right before the try/except statement completes. If a finally block contains a return statement, its return value takes strict precedence and will silently override any return values previously executed in the try or except blocks."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Exception Handling and the Finally Block",
                "scenario": "What will be the output of the following function call?\n\n```python\ndef fetch_data():\n    try:\n        return \"Try Block\"\n    except Exception:\n        return \"Except Block\"\n    finally:\n        return \"Finally Block\"\n\nprint(fetch_data())\n```",
                "hint": "Consider the execution guarantee of the `finally` block. If `finally` contains a return statement, how does it interact with return statements triggered earlier in the `try` block?",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of the `finally` execution guarantee", "Knowledge of control flow overrides and return statement precedence"],
                "solution_code": 'result = "Finally Block"',
                "expected_output": 'Finally Block',
                "big_o_explanation": "O(1) - Exception handling and block transitions operate in constant time.",
                "follow_up_probes": ["What happens if an exception is raised in the `try` block, but the `finally` block returns a value instead of re-raising it?", "Why is it considered an anti-pattern to return from a `finally` block?"]
            }
        ]
    }
