import pandas as pd

def get_exercise():
    return {
        "title": "List Comprehensions and Filtering",
        "subtitle": "comprehensions",
        "description": "Given a list of dictionaries representing student records, how can you extract the names of students who scored above 90 in their mathematics exam?\n\n```python\nrecords = [\n    {\"name\": \"Alice\", \"math_score\": 92},\n    {\"name\": \"Bob\", \"math_score\": 85},\n    {\"name\": \"Charlie\", \"math_score\": 88},\n    {\"name\": \"David\", \"math_score\": 91},\n    {\"name\": \"Eve\", \"math_score\": 95}\n]\n```",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "Review the syntax for list comprehensions: `[expression for item in iterable if condition]`.",
        "solution_python": "result = [student['name'] for student in records if student['math_score'] > 90]",
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis tests your ability to fluently write list comprehensions while respecting Python's dictionary access patterns.\n\n* **Syntax Breakdown:** The structure `[expression for item in iterable if condition]` allows you to filter and map in a single pass. \n* **Correct Access:** `student['name']` is the correct way to access values in a dictionary. \n* **Common Pitfalls:** \n    * Option B is incorrect because Python dictionaries do not support dot notation (e.g., `record.name`) for key access; this would raise an `AttributeError`.\n    * Option C is incorrect because it tries to index the list `records` directly instead of the loop variable, and references a non-existent `subject` key.\n    * Option D is incorrect because it uses `>= 90`, which would include students who scored exactly 90, violating the \"above 90\" requirement.",
        "big_o_explanation": "O(n) - The list comprehension iterates through the `records` list once, evaluating the condition and mapping the output.",
        "mcq_questions": [
             {
                 "question": "Select Correct Answers:",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "[student['name'] for student in records if student['math_score'] > 90]", "is_correct": True},
                     {"label": "B", "text": "[record.name for record in records if record['math_score'] > 90]", "is_correct": False},
                     {"label": "C", "text": "[name for name in records if records['math_score'] > 90 and name['subject'] == 'Mathematics']", "is_correct": False},
                     {"label": "D", "text": "[student['name'] for student in records if student['math_score'] >= 90]", "is_correct": False},
                 ],
                 "explanation": "Option A is correct because it uses the proper syntax for both list comprehensions and dictionary key access. Option B fails because Python dictionaries do not support dot notation (`record.name`)."
             }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "Given a list of dictionaries representing student records, how can you extract the names of students who scored above 90 in their mathematics exam?\n\n```python\nrecords = [\n    {\"name\": \"Alice\", \"math_score\": 92},\n    {\"name\": \"Bob\", \"math_score\": 85},\n    {\"name\": \"Charlie\", \"math_score\": 88},\n    {\"name\": \"David\", \"math_score\": 91},\n    {\"name\": \"Eve\", \"math_score\": 95}\n]\n```",
                "hint": "Review the syntax for list comprehensions: `[expression for item in iterable if condition]`.",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Ability to write pythonic list comprehensions", "Understanding of iterable unpacking"],
                "solution_code": "result = [student['name'] for student in records if student['math_score'] > 90]",
                "expected_output": 'Options A and B',
                "big_o_explanation": "O(n) - Single pass through the iterable.",
                "follow_up_probes": ["What if the math_score key is missing from some dictionaries? How would you handle it?"]
            }
        ]
    }
