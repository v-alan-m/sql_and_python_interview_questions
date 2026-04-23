import pandas as pd

def get_exercise():
    return {
        "title": "Lexical Scoping and Closures",
        "subtitle": "closures",
        "description": "Consider the following Python code:\nWhat will be the value of the result after executing the above code?\n\n```python\ndef outer_func(x):\n    def inner_func(y):\n        return x + y\n    return inner_func\n\nresult = outer_func(5)(3)\n```",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": pd.DataFrame({"x_value": [5], "y_value": [3]}),
        "allowed_modes": ["Python"],
        "hint_python": "Notice that `outer_func(5)` returns a function. The `(3)` immediately calls that returned function. What value of `x` does `inner_func` remember?",
        "solution_python": "result = 8",
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

This exercise targets the concept of **Closures**. A closure occurs when an inner function "closes over" or remembers the state of variables in its enclosing scope, even after the outer function has finished executing.

When we evaluate `outer_func(5)`:
1. Python creates the local variable `x = 5`.
2. Python defines the nested function `inner_func(y)`.
3. Because `inner_func` references `x`, Python creates a closure binding the value `5` to the `x` variable inside `inner_func`'s `__closure__` attribute.
4. The outer function returns the *reference* to `inner_func` and immediately exits. The local scope of `outer_func` is destroyed, but the bound value of `x` survives inside the closure.

The second set of parentheses `(3)` immediately invokes that returned function, passing `3` as `y`.
Inside `inner_func`, it evaluates `x + y`. It pulls `x` (which is `5`) from its closure, and uses the local argument `y` (which is `3`). `5 + 3 = 8`.

Closures are the foundational mechanism that allows function decorators to work in Python.

- Option B, C, and D are incorrect as they evaluate different arithmetic combinations not represented by `5 + 3`.""",
        "big_o_explanation": "O(1) - Defining and executing the closure operates in constant time.",
        
        "mcq_questions": [
             {
                 "question": "What will be the value of the result after executing the closure code?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "8", "is_correct": True},
                     {"label": "B", "text": "15", "is_correct": False},
                     {"label": "C", "text": "53", "is_correct": False},
                     {"label": "D", "text": "35", "is_correct": False},
                 ],
                 "explanation": "This tests closures. `outer_func(5)` returns `inner_func`, which \"remembers\" that `x` is 5 in its enclosing scope. The second pair of parentheses `(3)` immediately calls that returned `inner_func` with `y` equal to 3. It returns 5 + 3, which is 8."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Lexical Scoping and Closures",
                "scenario": "Consider the following Python code:\nWhat will be the value of the result after executing the above code?\n\n```python\ndef outer_func(x):\n    def inner_func(y):\n        return x + y\n    return inner_func\n\nresult = outer_func(5)(3)\n```",
                "hint": "Notice that `outer_func(5)` returns a function. The `(3)` immediately calls that returned function. What value of `x` does `inner_func` remember?",
                "data": pd.DataFrame({"x_value": [5], "y_value": [3]}),
                "evaluation_criteria": ["Understanding of function closures", "Knowledge of lexical scoping and variable lifetime"],
                "solution_code": "result = 8",
                "expected_output": 8,
                "big_o_explanation": "O(1) - Defining and executing the closure operates in constant time.",
                "follow_up_probes": ["Where exactly does Python store the bound variable `x` on the function object?", "How does the `nonlocal` keyword interact with closures?"]
            }
        ]
    }
