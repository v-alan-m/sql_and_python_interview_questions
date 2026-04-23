import pandas as pd

def get_exercise():
    return {
        "title": "List Comprehensions and Filtering",
        "subtitle": "comprehensions",
        "description": "Given a list of dictionaries representing student records, how can you extract the names of students who scored above 90 in their mathematics exam?\n\n```python\nrecords = [\n    {\"name\": \"Alice\", \"math_score\": 92},\n    {\"name\": \"Bob\", \"math_score\": 85},\n    {\"name\": \"Charlie\", \"math_score\": 88},\n    {\"name\": \"David\", \"math_score\": 91},\n    {\"name\": \"Eve\", \"math_score\": 95}\n]\n```\n\nSelect Correct Answers:\nA) `[student['name'] for student in records if student['math_score'] > 90]`\nB) `[record['name'] for record in records if record['math_score'] > 90]`\nC) `[name for name in records if records['math_score'] > 90 and name['subject'] == 'Mathematics']`\nD) `[student['name'] for student in records if student['math_score'] >= 90]`",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": pd.DataFrame({"id": [1, 2], "input": ["a", "b"]}),
        "allowed_modes": ["Python"],
        "hint_python": "Review the syntax for list comprehensions: `[expression for item in iterable if condition]`.",
        "solution_python": 'result = "Options A and B"',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis tests your ability to fluently write list comprehensions, a hallmark of idiomatic Python.\n\n* **Syntax Breakdown:** The structure `[expression for item in iterable if condition]` allows you to filter and map in a single pass. \n* **Mapping:** `student['name']` extracts the specific value from the dictionary.\n* **Condition:** `if student['math_score'] > 90` ensures we strictly only process records meeting the 90 threshold.\n* **Variable Naming:** The loop variable name (`student` vs `record`) does not alter the execution logic, making both Option A and Option B functionally identical and correct.\n\nUsing comprehensions over traditional `for` loops in Python is generally faster because they are optimized in C underneath.",
        "big_o_explanation": "O(n) - The list comprehension iterates through the `records` list once, evaluating the condition and mapping the output.",
        "mcq_questions": [
             {
                 "question": "Select Correct Answers:",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "[student['name'] for student in records if student['math_score'] > 90]", "is_correct": True},
                     {"label": "B", "text": "[record['name'] for record in records if record['math_score'] > 90]", "is_correct": True},
                     {"label": "C", "text": "[name for name in records if records['math_score'] > 90 and name['subject'] == 'Mathematics']", "is_correct": False},
                     {"label": "D", "text": "[student['name'] for student in records if student['math_score'] >= 90]", "is_correct": False},
                 ],
                 "explanation": "List comprehensions follow the syntax `[expression for item in iterable if condition]`. Both A and B correctly iterate through 'records', check if the specific dictionary's 'math_score' is strictly greater than 90, and extract the 'name'."
             }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "Given a list of dictionaries representing student records, how can you extract the names of students who scored above 90 in their mathematics exam?\n\n```python\nrecords = [\n    {\"name\": \"Alice\", \"math_score\": 92},\n    {\"name\": \"Bob\", \"math_score\": 85},\n    {\"name\": \"Charlie\", \"math_score\": 88},\n    {\"name\": \"David\", \"math_score\": 91},\n    {\"name\": \"Eve\", \"math_score\": 95}\n]\n```\n\nSelect Correct Answers:\nA) `[student['name'] for student in records if student['math_score'] > 90]`\nB) `[record['name'] for record in records if record['math_score'] > 90]`\nC) `[name for name in records if records['math_score'] > 90 and name['subject'] == 'Mathematics']`\nD) `[student['name'] for student in records if student['math_score'] >= 90]`",
                "hint": "Review the syntax for list comprehensions: `[expression for item in iterable if condition]`.",
                "data": pd.DataFrame({"id": [1], "input": ["c"]}),
                "evaluation_criteria": ["Ability to write pythonic list comprehensions", "Understanding of iterable unpacking"],
                "solution_code": 'result = "Options A and B"',
                "expected_output": 'Options A and B',
                "big_o_explanation": "O(n) - Single pass through the iterable.",
                "follow_up_probes": ["What if the math_score key is missing from some dictionaries? How would you handle it?"]
            }
        ]
    }
