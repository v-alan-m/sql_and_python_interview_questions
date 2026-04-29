import pandas as pd

def get_exercise():
    return {
        "title": "Control Flow and State Tracking",
        "subtitle": "control-flow",
        "description": "What will be the output of the following Python code?",
        "difficulty_level": "mid",
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
        "hint_python": "Walk through the loop, noting the total when each score (even vs. odd) is processed.",
        "solution_python": 'result = 160',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis question ensures you can mentally trace conditional logic within iterative loops, a fundamental debugging skill.\n\n* **Even Numbers Handling:** The `if score % 2 == 0` check targets 10, 20, and 30. These are doubled before adding to the total: `(10 * 2) + (20 * 2) + (30 * 2) = 20 + 40 + 60 = 120`.\n* **Odd Numbers Handling:** The `else` block targets 15 and 25. These are added directly: `15 + 25 = 40`.\n* **Final Calculation:** Combining both logic branches gives the result: `120 + 40 = 160`.\n\nWhile simple, recognizing patterns like modulo arithmetic and accumulating state is central to almost all algorithms.",
        "big_o_explanation": "O(n) - We perform a constant time O(1) mathematical operation for each element in the input list.",
        "mcq_questions": [
             {
                 "question": "What will be the output of the following Python code?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "145", "is_correct": False},
                     {"label": "B", "text": "160", "is_correct": True},
                     {"label": "C", "text": "155", "is_correct": False},
                     {"label": "D", "text": "165", "is_correct": False},
                 ],
                 "explanation": "The loop checks for even numbers using the modulo operator (%). Evens (10, 20, 30) are doubled and added to the total (20 + 40 + 60 = 120). Odds (15, 25) are added directly (15 + 25 = 40). 120 + 40 = 160."
             }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "What will be the output of the following Python code?",
                "hint": "Walk through the loop, noting the total when each score (even vs. odd) is processed.",
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
                "evaluation_criteria": ["Ability to mentally trace code execution", "Understanding of modulo operator"],
                "solution_code": 'result = 160',
                "expected_output": 160,
                "big_o_explanation": "O(n) - Single loop over the elements.",
                "follow_up_probes": ["Could you refactor this into a single return statement using a list comprehension or generator expression?"]
            }
        ]
    }
