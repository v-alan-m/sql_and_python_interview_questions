import pandas as pd

def get_exercise():
    return {
        "title": "Set Operations and Intersections",
        "subtitle": "sets",
        "description": "What is the result of the following set operations?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """s1 = {10, 20, 30, 40}
s2 = {30, 40, 50, 60}
result = (s1 | s2) - (s1 & s2)
print(result)""",
        "hide_data": False,
        "allowed_modes": ["Python"],
        "hint_python": "Calculate the Union `|` first, then calculate the Intersection `&`, and finally subtract the two sets.",
        "solution_python": 'result = "{10, 20, 50, 60}"',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis question evaluates your fluency with native mathematical set operations, which are heavily utilized in data engineering and cleaning.\n\n* **Union (`|`):** The expression `s1 | s2` merges the two sets, retaining only unique elements. The result is `{10, 20, 30, 40, 50, 60}`.\n* **Intersection (`&`):** The expression `s1 & s2` identifies the elements that exist in *both* sets. The result is `{30, 40}`.\n* **Difference (`-`):** The difference operator subtracts the elements of the right set from the left set. Therefore, removing `{30, 40}` from `{10, 20, 30, 40, 50, 60}` leaves `{10, 20, 50, 60}`.\n\n*Pro-tip:* The formula `(A | B) - (A & B)` calculates the **Symmetric Difference** (elements in either set A or set B, but not both). In Python, this operation is built-in and can be optimized using the caret operator: `s1 ^ s2`.",
        "big_o_explanation": "O(N) - Set operations run in O(len(s1) + len(s2)) time.",
        "mcq_questions": [
             {
                 "question": "What is the result of the following set operations?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "{10, 20, 50, 60}", "is_correct": True},
                     {"label": "B", "text": "{30, 40}", "is_correct": False},
                     {"label": "C", "text": "{10, 20, 30, 40, 50, 60}", "is_correct": False},
                     {"label": "D", "text": "{}", "is_correct": False},
                 ],
                 "explanation": "s1 | s2 (Union) combines all unique elements: {10, 20, 30, 40, 50, 60}. s1 & s2 (Intersection) finds common elements: {30, 40}. The difference operator (-) subtracts the intersection from the union, leaving {10, 20, 50, 60}. Note: This is the Symmetric Difference, which can be optimized in Python using the ^ operator (s1 ^ s2)."
             }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "What is the result of the following set operations?",
                "hint": "Calculate the Union `|` first, then calculate the Intersection `&`, and finally subtract the two sets.",
                "data": """s1 = {10, 20, 30, 40}
s2 = {30, 40, 50, 60}
result = (s1 | s2) - (s1 & s2)
print(result)""",
                "hide_data": False,
                "evaluation_criteria": ["Understanding of set union, intersection, difference", "Knowledge of symmetric difference"],
                "solution_code": 'result = "{10, 20, 50, 60}"',
                "expected_output": '{10, 20, 50, 60}',
                "big_o_explanation": "O(N) - The operations require hashing and iterating elements of both sets.",
                "follow_up_probes": ["Is there a single operator that can perform this exact operation in Python?"]
            }
        ]
    }
