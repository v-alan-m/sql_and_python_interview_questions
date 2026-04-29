import pandas as pd

def get_exercise():
    return {
        "title": "First-Class Functions",
        "subtitle": "first-class-functions",
        "description": "Consider the following Python function:\nWhat will be the output of the result list?",
        "difficulty_level": "easy",
        "source_inspiration": "Anki Deck",
        "data": """def custom_map(func, lst):
    return [func(item) for item in lst]

def add_ten(num):
    return num + 10

numbers = [1, 2, 3, 4, 5]
result = custom_map(add_ten, numbers)""",
        "hide_data": False,
        "allowed_modes": ["Python"],
        "hint_python": "Notice how the `add_ten` function is passed without parentheses. It is being executed dynamically inside `custom_map` via a list comprehension.",
        "solution_python": "result = [11, 12, 13, 14, 15]",
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

One of Python's most powerful paradigms is that **functions are first-class citizens**. This means that under the hood, a function is just an object (specifically, an instance of the `function` class). 

Because functions are just objects, you can do anything with them that you would do with an integer or a string:
1. Assign them to variables.
2. Store them in data structures (like lists or dictionaries).
3. **Pass them as arguments to other functions** (Higher-Order Functions).
4. Return them from other functions (Closures/Decorators).

In this script, `add_ten` is passed to `custom_map` as an argument without parentheses. We are passing the *reference* to the function, not invoking it.

Inside `custom_map`, the list comprehension `[func(item) for item in lst]` iterates through `[1, 2, 3, 4, 5]`. For each `item`, it invokes the passed function (`add_ten(item)`). 
- `add_ten(1)` -> 11
- `add_ten(2)` -> 12
- `add_ten(3)` -> 13
- `add_ten(4)` -> 14
- `add_ten(5)` -> 15

The resulting list is `[11, 12, 13, 14, 15]`. This mimics the behavior of Python's built-in `map()` function.

- Option A is incorrect as it multiplies by 10 instead of adding 10.
- Option C is incorrect as it returns the original list unmodified.
- Option D is incorrect as it adds 20 instead of 10.""",
        "big_o_explanation": "O(N) - The list comprehension must iterate through each of the N items in the list exactly once.",
        
        "mcq_questions": [
             {
                 "question": "What will be the output of the result list after applying the custom map function?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "[10, 20, 30, 40, 50]", "is_correct": False},
                     {"label": "B", "text": "[11, 12, 13, 14, 15]", "is_correct": True},
                     {"label": "C", "text": "[1, 2, 3, 4, 5]", "is_correct": False},
                     {"label": "D", "text": "[21, 22, 23, 24, 25]", "is_correct": False},
                 ],
                 "explanation": "Functions are first-class citizens in Python and can be passed as arguments. The `custom_map` function takes `add_ten` and applies it to each item in the list via a list comprehension. Adding 10 to each element of `[1, 2, 3, 4, 5]` results in `[11, 12, 13, 14, 15]`."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "First-Class Functions",
                "scenario": "Consider the following Python function:\nWhat will be the output of the result list?",
                "hint": "Notice how the `add_ten` function is passed without parentheses. It is being executed dynamically inside `custom_map` via a list comprehension.",
                "data": """def custom_map(func, lst):
    return [func(item) for item in lst]

def add_ten(num):
    return num + 10

numbers = [1, 2, 3, 4, 5]
result = custom_map(add_ten, numbers)""",
                "hide_data": False,
                "evaluation_criteria": ["Understanding of functions as first-class objects", "Ability to trace higher-order function execution and list comprehensions"],
                "solution_code": "result = [11, 12, 13, 14, 15]",
                "expected_output": [11, 12, 13, 14, 15],
                "big_o_explanation": "O(N) - The list comprehension must iterate through each of the N items in the list exactly once.",
                "follow_up_probes": ["Can you rewrite this using Python's built-in `map()` and a `lambda` function?", "What is the difference between a first-class function and a higher-order function?"]
            }
        ]
    }
