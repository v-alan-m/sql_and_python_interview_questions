import pandas as pd

def get_exercise():
    return {
        "title": "Decorator Fundamentals",
        "subtitle": "decorators",
        "description": "Which of the given statements about Python decorators is true?",
        "difficulty_level": "easy",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "Think about why decorators are used. Are they strictly limited to certain functions, or are they a general-purpose design pattern?",
        "solution_python": 'result = "Decorators are primarily used to modify or enhance the behavior of a function without explicitly modifying its internal implementation."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

At a system architecture level, decorators implement the **Decorator Design Pattern**. They provide a clean, Pythonic way to adhere to the Open/Closed Principle (software entities should be open for extension, but closed for modification).

By wrapping a function with a decorator, you dynamically inject new behavior (like authentication checks, logging, caching, or timing) before, during, or after the target function executes. You accomplish this without ever touching the source code of the target function itself.

Because Python functions are first-class objects, a decorator is simply a higher-order function that takes a function as input and returns a new callable wrapper.

- Option A is incorrect because decorators can accept functions with any number of arguments (using `*args, **kwargs`).
- Option B is incorrect because the `@decorator` syntax is just "syntactic sugar." You can manually apply a decorator by executing `func = my_decorator(func)`.
- Option D is incorrect because decorators can absolutely be stacked or chained (e.g., applying `@login_required` and then `@log_activity`). When stacked, they evaluate from the bottom up.""",
        "big_o_explanation": "O(1) - Applying a decorator takes constant time during module initialization.",
        
        "mcq_questions": [
             {
                 "question": "Which of the given statements about Python decorators is true?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "Decorators can only be applied to functions that do not take any arguments.", "is_correct": False},
                     {"label": "B", "text": "Decorators can only be defined using the @decorator syntax in Python.", "is_correct": False},
                     {"label": "C", "text": "Decorators are primarily used to modify or enhance the behavior of a function without explicitly modifying its internal implementation.", "is_correct": True},
                     {"label": "D", "text": "Decorators cannot be stacked, i.e., you can not apply multiple decorators to a single function.", "is_correct": False},
                 ],
                 "explanation": "A decorator is a function that takes another function as an argument, adds functionality (like logging or timing), and returns a wrapper function, all without altering the original function's source code."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Decorator Fundamentals",
                "scenario": "Which of the given statements about Python decorators is true?",
                "hint": "Think about why decorators are used. Are they strictly limited to certain functions, or are they a general-purpose design pattern?",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of the decorator design pattern", "Knowledge of decorator flexibility and syntactic sugar mechanics"],
                "solution_code": 'result = "Decorators are primarily used to modify or enhance the behavior of a function without explicitly modifying its internal implementation."',
                "expected_output": 'Decorators are primarily used to modify or enhance the behavior of a function without explicitly modifying its internal implementation.',
                "big_o_explanation": "O(1) - Applying a decorator takes constant time during module initialization.",
                "follow_up_probes": ["What happens if you stack two decorators? Which one executes first?", "How do you pass arguments to a decorator itself?"]
            }
        ]
    }
