import pandas as pd

def get_exercise():
    return {
        "title": "Control Flow and Iteration",
        "subtitle": "control-flow",
        "description": "What will be the output of the following Python code?",
        "difficulty_level": "easy",
        "source_inspiration": "Anki Deck",
        "data": """def calculate_total_score(scores):
    total = 0
    for score in scores:
        if score % 2 == 0:
            total += score * 2
        else:
            total += score
    return total

student_scores = [10, 15, 20, 25, 30]
result = calculate_total_score(student_scores)
print(result)""",
        "hide_data": False,
        "allowed_modes": ["Python"],
        "hint_python": "Trace the loop step by step. If a number is even, double it and add it. If it is odd, add it as-is.",
        "solution_python": "result = 160",
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

Control flow structures (loops and conditionals) form the basic logic of any program. This specific exercise tests the ability to mentally trace state mutation inside a `for` loop combined with a modulus conditional.

Let's break down the iteration over `[10, 15, 20, 25, 30]`:
1. **10**: `10 % 2 == 0` evaluates to `True`. `total += 10 * 2` -> `total` is `20`.
2. **15**: `15 % 2 == 0` evaluates to `False`. `total += 15` -> `total` is `20 + 15 = 35`.
3. **20**: `20 % 2 == 0` evaluates to `True`. `total += 20 * 2` -> `total` is `35 + 40 = 75`.
4. **25**: `25 % 2 == 0` evaluates to `False`. `total += 25` -> `total` is `75 + 25 = 100`.
5. **30**: `30 % 2 == 0` evaluates to `True`. `total += 30 * 2` -> `total` is `100 + 60 = 160`.

The final accumulated total is `160`.

- Option A (145) is incorrect because it fails to properly accumulate the odds or evens.
- Option C (155) is incorrect; an arithmetic tracing error.
- Option D (165) is incorrect; another arithmetic tracing error.""",
        "big_o_explanation": "O(N) - The algorithm iterates over the list of N scores exactly once, performing constant-time arithmetic operations in each step.",
        
        "mcq_questions": [
             {
                 "question": "What will be the output of the provided Python code calculating total scores?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "145", "is_correct": False},
                     {"label": "B", "text": "160", "is_correct": True},
                     {"label": "C", "text": "155", "is_correct": False},
                     {"label": "D", "text": "165", "is_correct": False},
                 ],
                 "explanation": "The code iterates through the list, checking for even numbers (`score % 2 == 0`). Evens are doubled before being added to `total`, while odds are added as-is. 10(even)->20, 15(odd)->15, 20(even)->40, 25(odd)->25, 30(even)->60. 20+15+40+25+60 = 160."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Control Flow and Iteration",
                "scenario": "What will be the output of the following Python code?",
                "hint": "Trace the loop step by step. If a number is even, double it and add it. If it is odd, add it as-is.",
                "data": """def calculate_total_score(scores):
    total = 0
    for score in scores:
        if score % 2 == 0:
            total += score * 2
        else:
            total += score
    return total

student_scores = [10, 15, 20, 25, 30]
result = calculate_total_score(student_scores)
print(result)""",
                "hide_data": False,
                "evaluation_criteria": ["Ability to mentally trace loops and conditionals", "Understanding of the modulus operator"],
                "solution_code": "result = 160",
                "expected_output": 160,
                "big_o_explanation": "O(N) - The algorithm iterates over the list of N scores exactly once, performing constant-time arithmetic operations in each step.",
                "follow_up_probes": ["Can you rewrite this using a generator expression inside `sum()`?", "What happens if a floating point number is passed in?"]
            }
        ]
    }
