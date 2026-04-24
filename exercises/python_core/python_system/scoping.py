import pandas as pd

def get_exercise():
    return {
        "title": "The nonlocal Keyword and Scoping",
        "subtitle": "scoping",
        "description": "What is the output of the following script that uses the nonlocal keyword?\n\n```python\ndef outer_func():\n    x = \"outer\"\n    def inner_func():\n        nonlocal x\n        x = \"inner\"\n    inner_func()\n    print(x)\n\nouter_func()\n```",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "Review the LEGB (Local, Enclosing, Global, Built-in) rule and what `nonlocal` explicitly targets.",
        "solution_python": 'result = "inner"',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis question evaluates your understanding of Python's LEGB variable resolution scoping rules and closure mutation.\n\n* **Default Scope Behavior:** Normally, if you assign a value to a variable inside a function (`x = \"inner\"`), Python assumes you are creating a completely new local variable. It will shadow the `x` defined in the outer scope, leaving the original `x` untouched.\n* **The `nonlocal` Keyword:** By declaring `nonlocal x` inside `inner_func`, you are explicitly instructing Python: 'Do not create a new local variable. Instead, look up the scope chain to the nearest enclosing function (`outer_func`), find the variable `x` there, and bind my local operations to that existing variable.'\n* **Mutation:** The line `x = \"inner\"` therefore mutates the variable `x` existing in `outer_func`. When `print(x)` is subsequently called in the outer scope, the value has been permanently altered to `'inner'`.\n\nThis is a critical pattern when maintaining state in decorator functions without resorting to class-based objects or risky global variables.",
        "big_o_explanation": "O(1) - Variable resolution and assignment occur in constant time.",
        "mcq_questions": [
             {
                 "question": "What is the output of the following script that uses the nonlocal keyword?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "outer", "is_correct": False},
                     {"label": "B", "text": "It raises a SyntaxError.", "is_correct": False},
                     {"label": "C", "text": "inner", "is_correct": True},
                     {"label": "D", "text": "The script has no output.", "is_correct": False},
                 ],
                 "explanation": "This tests the LEGB rule and closures. The nonlocal keyword inside inner_func() tells Python not to create a new local variable x, but to look up the enclosing scope (outer_func) and bind to the existing x. Thus, x = 'inner' modifies the outer variable permanently. When outer_func() calls print(x), the value has been changed to 'inner'."
             }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "What is the output of the following script that uses the nonlocal keyword?\n\n```python\ndef outer_func():\n    x = \"outer\"\n    def inner_func():\n        nonlocal x\n        x = \"inner\"\n    inner_func()\n    print(x)\n\nouter_func()\n```",
                "hint": "Review the LEGB (Local, Enclosing, Global, Built-in) rule and what `nonlocal` explicitly targets.",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of Python scope (LEGB)", "Knowledge of nonlocal vs global"],
                "solution_code": 'result = "inner"',
                "expected_output": 'inner',
                "big_o_explanation": "O(1) - Constant execution time.",
                "follow_up_probes": ["What is the difference between `nonlocal` and `global`?"]
            }
        ]
    }
