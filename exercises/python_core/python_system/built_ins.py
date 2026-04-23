import pandas as pd

def get_exercise():
    return {
        "title": "Built Ins",
        "subtitle": "Built Ins",
        "description": """What does the following print function call output to the console?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """\
print('python', 'is', 'fun', sep='-', end='!')""",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = "python-is-fun!"',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**
This question tests your understanding of the keyword arguments available within Python's built-in `print()` function. As a lead engineer, it's crucial to be intimately familiar with the standard library signatures to avoid writing unnecessary boilerplate string concatenation.

Here is the breakdown of the function call `print('python', 'is', 'fun', sep='-', end='!')`:

* **Positional Arguments (`*objects`):** The function is passed three distinct string objects: `'python'`, `'is'`, and `'fun'`.
* **The `sep` Argument:** By default, `print()` separates multiple objects with a single space (`' '`). By explicitly setting `sep='-'`, you are instructing Python to join the positional arguments using a hyphen. This evaluates the core string to `python-is-fun`.
* **The `end` Argument:** By default, `print()` appends a newline character (`'\n'`) at the end of the output. By setting `end='!'`, you override this behavior, telling Python to append an exclamation mark instead of moving to a new line. Notice there are no spaces in the `end` string provided.

Combining these behaviors, the items are joined by hyphens, and the exclamation mark is immediately appended at the end without any trailing spaces, resulting precisely in `python-is-fun!`.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """What does the following print function call output to the console?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """python-is-fun!""", "is_correct": True},
                     {"label": "B", "text": """python is fun!""", "is_correct": False},
                     {"label": "C", "text": """python, is, fun!""", "is_correct": False},
                     {"label": "D", "text": """python-is-fun !""", "is_correct": True},
                 ],
                 "explanation": """The print() function joins positional string arguments using the string provided to the sep keyword argument (a hyphen). It ends the output with the string provided to the end keyword argument (an exclamation mark) instead of the default newline."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """What does the following print function call output to the console?

""",
                "hint": "Remember that print() accepts multiple positional arguments and specific keyword arguments to control its formatting behavior.",
                "data": """\
print('python', 'is', 'fun', sep='-', end='!')""",
                "evaluation_criteria": ["Fluency with standard library built-ins", "Understanding of *args and **kwargs implementation", "Code efficiency and readability"],
                "solution_code": 'result = "python-is-fun!"',
                "expected_output": "python-is-fun!",
                "big_o_explanation": "O(N) Time where N is the total length of the strings being joined and printed.",
                "follow_up_probes": ["How would you implement a custom logger that mimics this exact signature?", "What happens if you pass a generator expression as the positional argument?"]
            }
        ]
    }
