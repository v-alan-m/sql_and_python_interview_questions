import pandas as pd

def get_exercise():
    return {
        "title": "Preserving Function Metadata in Decorators",
        "subtitle": "decorators",
        "description": "You are writing a logging decorator for a framework, but users complain that their function docstrings and names are disappearing. Look at the code:\n\n```python\nimport functools\n\ndef log_call(func):\n    def wrapper(*args, **kwargs):\n        \"\"\"Wrapper docstring\"\"\"\n        print(f\"Calling {func.__name__}\")\n        return func(*args, **kwargs)\n    return wrapper\n\n@log_call\ndef calculate_tax(amount):\n    \"\"\"Calculates standard tax.\"\"\"\n    return amount * 0.2\n\nprint(calculate_tax.__name__)\n```\n\nWhat does the print statement currently output, and how do you fix it at the system level?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": pd.DataFrame({"function": ["calculate_tax"], "docstring": ["Calculates standard tax."], "is_decorated": [True]}),
        "allowed_modes": ["Python"],
        "hint_python": "Decorators fundamentally replace the target function with the wrapper function. How do you copy the metadata from the original function back to the wrapper?",
        "solution_python": 'result = "Output: wrapper. Fix: Add @functools.wraps(func) directly above the \'def wrapper\' definition to copy the original function\'s metadata."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

To master decorators, you must recognize that the `@decorator` syntax is simply syntactic sugar for `calculate_tax = log_call(calculate_tax)`. 

When `log_call` executes, it dynamically defines and returns a brand-new function called `wrapper`. This `wrapper` function completely overrides the original `calculate_tax` reference. Because it is a completely separate function, it carries its own metadata—namely, its name (`"wrapper"`) and its docstring (`"Wrapper docstring"`).

This is highly problematic for frameworks, introspection tools (like `help()`), and debuggers, which rely heavily on accurate docstrings and function names.

The standard library `functools` provides the solution: `@functools.wraps`.
When you decorate the `wrapper` function with `@wraps(func)`, you are instructing Python to intelligently copy critical dunder attributes (`__module__`, `__name__`, `__qualname__`, `__doc__`, and `__annotations__`) from the original `func` directly onto the `wrapper`. 

This creates a seamless illusion: the function behaves with the new wrapper logic, but introspection tools see the original function's identity.

- Option A is incorrect because `calculate_tax` is unequivocally replaced, so it will output `wrapper`.
- Option C is incorrect because while manually reassigning `wrapper.__name__ = func.__name__` works for the name, it fails to comprehensively copy docstrings, annotations, and other critical metadata.
- Option D is syntactically invalid and misunderstands how decorators accept callable arguments.""",
        "big_o_explanation": "O(1) - Applying `@functools.wraps` performs a simple constant-time attribute copy during function definition.",
        
        "mcq_questions": [
             {
                 "question": "What does the print statement currently output, and how do you fix it at the system level?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "Output: calculate_tax. Fix: No fix needed.", "is_correct": False},
                     {"label": "B", "text": "Output: wrapper. Fix: Add @functools.wraps(func) directly above the 'def wrapper' definition to copy the original function's metadata.", "is_correct": True},
                     {"label": "C", "text": "Output: log_call. Fix: Add wrapper.__name__ = func.__name__ inside the wrapper function body.", "is_correct": False},
                     {"label": "D", "text": "Output: wrapper. Fix: Pass the calculate_tax function as an explicit string to the decorator.", "is_correct": False},
                 ],
                 "explanation": "A decorator essentially replaces the original function with the wrapper function. Without @functools.wraps, introspection tools (like help() or __name__) will only see the name 'wrapper' and its 'Wrapper docstring'. The @wraps decorator safely copies crucial metadata (__module__, __name__, __qualname__, __doc__) from the original function to the new wrapper."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Preserving Function Metadata in Decorators",
                "scenario": "You are writing a logging decorator for a framework, but users complain that their function docstrings and names are disappearing. Look at the code:\n\n```python\nimport functools\n\ndef log_call(func):\n    def wrapper(*args, **kwargs):\n        \"\"\"Wrapper docstring\"\"\"\n        print(f\"Calling {func.__name__}\")\n        return func(*args, **kwargs)\n    return wrapper\n\n@log_call\ndef calculate_tax(amount):\n    \"\"\"Calculates standard tax.\"\"\"\n    return amount * 0.2\n\nprint(calculate_tax.__name__)\n```\n\nWhat does the print statement currently output, and how do you fix it at the system level?",
                "hint": "Decorators fundamentally replace the target function with the wrapper function. How do you copy the metadata from the original function back to the wrapper?",
                "data": pd.DataFrame({"function": ["calculate_tax"], "docstring": ["Calculates standard tax."], "is_decorated": [True]}),
                "evaluation_criteria": ["Understanding of function wrappers and metadata", "Proper application of functools.wraps"],
                "solution_code": 'result = "Output: wrapper. Fix: Add @functools.wraps(func) directly above the \'def wrapper\' definition to copy the original function\'s metadata."',
                "expected_output": "Output: wrapper. Fix: Add @functools.wraps(func) directly above the 'def wrapper' definition to copy the original function's metadata.",
                "big_o_explanation": "O(1) - Applying `@functools.wraps` performs a simple constant-time attribute copy during function definition.",
                "follow_up_probes": ["Can you retrieve the original, unwrapped function if `@functools.wraps` was used?", "How would you handle this in a class-based decorator?"]
            }
        ]
    }
