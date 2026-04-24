import pandas as pd

def get_exercise():
    return {
        "title": "Global Variable Scoping",
        "subtitle": "scoping",
        "description": "Which of the following is True about Python's `global` keyword?",
        "difficulty_level": "easy",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "By default, variables created inside a function belong exclusively to that function. What happens if you want to modify a variable defined at the top level of the module?",
        "solution_python": 'result = "It allows you to define a variable as global within a function, meaning it can be accessed from any scope."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

Python resolves variable names using the **LEGB rule** (Local, Enclosing, Global, Built-in). 

When you *read* a variable inside a function, Python automatically checks these scopes inside-out. You do not need any special keywords to read a global variable. However, when you *assign* a value to a variable inside a function (`my_var = 10`), Python's default behavior is to create a brand new **Local** variable, masking the global one.

The `global` keyword explicitly disables this default behavior. When you declare `global my_var` inside a function, you are telling the interpreter: *"Do not create a local variable named my_var. Instead, bind all assignments directly to the module-level variable named my_var."*

This makes the variable accessible and mutable across any scope within that module. However, relying heavily on `global` is considered an anti-pattern in software architecture, as it introduces hidden side-effects, makes testing difficult, and breaks encapsulation.

- Option B is incorrect because `global` explicitly *allows* outside variables to be modified.
- Option C is incorrect because `global` binds to the module's namespace, regardless of whether it is the "main" module or an imported one.
- Option D is incorrect because `global` declarations must occur *before* the variable is assigned within the function.""",
        "big_o_explanation": "O(1) - Namespace lookup and variable binding are constant time operations.",
        
        "mcq_questions": [
             {
                 "question": "Which of the following is True about Python's global keyword?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "It allows you to define a variable as global within a function, meaning it can be accessed from any scope.", "is_correct": True},
                     {"label": "B", "text": "It restricts the use of global variables inside a function, ensuring that no outside variable can be modified.", "is_correct": False},
                     {"label": "C", "text": "It can only be used within the main module of a Python program.", "is_correct": False},
                     {"label": "D", "text": "It is used to convert a local variable into a global one after a function has completed.", "is_correct": False},
                 ],
                 "explanation": "Variables created inside a function are local by default. The `global` keyword acts as a declaration, telling Python not to create a local variable but instead to map all assignments directly to the module-level variable of that name."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Global Variable Scoping",
                "scenario": "Which of the following is True about Python's `global` keyword?",
                "hint": "By default, variables created inside a function belong exclusively to that function. What happens if you want to modify a variable defined at the top level of the module?",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of Python's LEGB scope resolution rule", "Appropriate use-cases and anti-patterns regarding global variables"],
                "solution_code": 'result = "It allows you to define a variable as global within a function, meaning it can be accessed from any scope."',
                "expected_output": 'It allows you to define a variable as global within a function, meaning it can be accessed from any scope.',
                "big_o_explanation": "O(1) - Namespace lookup and variable binding are constant time operations.",
                "follow_up_probes": ["What is the difference between `global` and `nonlocal`?", "Why is using global variables considered a bad practice in large codebases?"]
            }
        ]
    }
