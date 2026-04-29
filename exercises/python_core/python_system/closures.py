import pandas as pd

def get_exercise():
    return {
        "title": "Lexical Closures",
        "subtitle": "closures",
        "description": "Consider the following Python code:\n\nWhat will be the value of the result after executing the above code?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """def outer_func(x):
    def inner_func(y):
        return x + y
    return inner_func

result = outer_func(5)(3)""",
        "hide_data": False,
        "allowed_modes": ["Python"],
        "hint_python": "Consider what value `outer_func(5)` returns, and what variables that returned function remembers from its environment.",
        "solution_python": 'result = 8',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis question evaluates your understanding of closures in Python.\n\n* **Higher-Order Functions:** `outer_func` is a higher-order function because it returns another function (`inner_func`).\n* **The Closure:** When `outer_func(5)` is called, it creates `inner_func` locally. However, `inner_func` references the variable `x` from its enclosing scope. Python recognizes this and creates a **closure**—a function object that retains the bindings of the free variables that exist in the lexical environment when it is created. It 'remembers' that `x` is 5.\n* **Execution:** `outer_func(5)` returns the `inner_func` closure. Then, we immediately invoke that returned closure with the argument `(3)`. Inside the closure, `x` is 5 (from memory) and `y` is 3 (from the current call), returning `5 + 3 = 8`.\n\nClosures are the foundational concept behind Python decorators and are widely used for data hiding and factory functions.",
        "big_o_explanation": "O(1) - Returning a function and executing an addition are both constant time operations.",
        "mcq_questions": [
             {
                 "question": "What will be the value of the result after executing the above code?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "8", "is_correct": True},
                     {"label": "B", "text": "15", "is_correct": False},
                     {"label": "C", "text": "53", "is_correct": False},
                     {"label": "D", "text": "35", "is_correct": False},
                 ],
                 "explanation": "This demonstrates a closure. outer_func(5) returns inner_func while retaining access to x=5 in its enclosing scope. Calling the returned function with (3) passes 3 as y, returning 5 + 3 = 8."
             }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "Consider the following Python code:\n\nWhat will be the value of the result after executing the above code?",
                "hint": "Consider what value `outer_func(5)` returns, and what variables that returned function remembers from its environment.",
                "data": """def outer_func(x):
    def inner_func(y):
        return x + y
    return inner_func

result = outer_func(5)(3)""",
                "hide_data": False,
                "evaluation_criteria": ["Understanding of lexical closures", "Understanding of higher-order functions"],
                "solution_code": 'result = 8',
                "expected_output": 8,
                "big_o_explanation": "O(1) - Constant execution time.",
                "follow_up_probes": ["Can a closure modify the value of a variable in its enclosing scope? If so, how?"]
            }
        ]
    }
