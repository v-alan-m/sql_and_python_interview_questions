import pandas as pd

def get_exercise():
    return {
        "title": "List Comprehensions with Conditionals",
        "subtitle": "comprehensions",
        "description": "Given a list of dictionaries representing student records, how can you extract the names of students who scored above 90 in their mathematics exam?\n\n```python\nrecords = [\n    {\"name\": \"Alice\", \"math_score\": 92},\n    {\"name\": \"Bob\", \"math_score\": 85},\n    {\"name\": \"Charlie\", \"math_score\": 88},\n    {\"name\": \"David\", \"math_score\": 91},\n    {\"name\": \"Eve\", \"math_score\": 95}\n]\n```",
        "difficulty_level": "easy",
        "source_inspiration": "Anki Deck",
        "data": pd.DataFrame({"name": ["Alice", "Bob", "Charlie", "David", "Eve"], "math_score": [92, 85, 88, 91, 95]}),
        "allowed_modes": ["Python"],
        "hint_python": "Review the syntax of list comprehensions: `[expression for item in iterable if condition]`.",
        "solution_python": 'result = "Options A and B"',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

List comprehensions provide a highly optimized, C-level implementation for mapping and filtering iterables in Python. They are inherently faster and more readable than equivalent `for` loops combined with `.append()` calls.

The standard syntax is: `[expression for item in iterable if condition]`.

Let's evaluate the correct options (A and B):
`[student['name'] for student in records if student['math_score'] > 90]`
`[record['name'] for record in records if record['math_score'] > 90]`

1. `for student in records`: This dictates the iteration over the list of dictionaries. The chosen variable name (`student` vs `record`) is arbitrary and merely acts as a local alias for the current item in the iteration.
2. `if student['math_score'] > 90`: This acts as the filter constraint. If the condition evaluates to `False`, the item is skipped.
3. `student['name']`: This is the evaluation expression that determines exactly what gets placed into the resulting list. We extract the string mapped to the `name` key.

- Option C is incorrect because it uses the list variable `records` in the condition instead of the item variable, which will raise a `TypeError`. It also references a non-existent `subject` key.
- Option D is incorrect because it uses `>= 90`, which includes students who scored exactly 90, violating the "above 90" requirement.""",
        "big_o_explanation": "O(N) - The comprehension must iterate through the entire list of N dictionaries exactly once to apply the filter and extract the names.",
        
        "mcq_questions": [
             {
                 "question": "Select the correct list comprehension syntaxes to extract names of students who scored above 90.",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "[student['name'] for student in records if student['math_score'] > 90]", "is_correct": True},
                     {"label": "B", "text": "[record['name'] for record in records if record['math_score'] > 90]", "is_correct": True},
                     {"label": "C", "text": "[name for name in records if records['math_score'] > 90 and name['subject'] == 'Mathematics']", "is_correct": False},
                     {"label": "D", "text": "[student['name'] for student in records if student['math_score'] >= 90]", "is_correct": False},
                 ],
                 "explanation": "List comprehensions follow the syntax [expression for item in iterable if condition]. Both A and B correctly iterate through 'records', check if the specific dictionary's 'math_score' is strictly greater than 90, and extract the 'name'."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "List Comprehensions with Conditionals",
                "scenario": "Given a list of dictionaries representing student records, how can you extract the names of students who scored above 90 in their mathematics exam?\n\n```python\nrecords = [\n    {\"name\": \"Alice\", \"math_score\": 92},\n    {\"name\": \"Bob\", \"math_score\": 85},\n    {\"name\": \"Charlie\", \"math_score\": 88},\n    {\"name\": \"David\", \"math_score\": 91},\n    {\"name\": \"Eve\", \"math_score\": 95}\n]\n```",
                "hint": "Review the syntax of list comprehensions: `[expression for item in iterable if condition]`.",
                "data": pd.DataFrame({"name": ["Alice", "Bob", "Charlie", "David", "Eve"], "math_score": [92, 85, 88, 91, 95]}),
                "evaluation_criteria": ["Understanding of list comprehension syntax", "Ability to map and filter data simultaneously"],
                "solution_code": 'result = "Options A and B"',
                "expected_output": 'Options A and B',
                "big_o_explanation": "O(N) - The comprehension must iterate through the entire list of N dictionaries exactly once to apply the filter and extract the names.",
                "follow_up_probes": ["How would you rewrite this as a dictionary comprehension?", "Why are list comprehensions generally faster than `for` loops in Python?"]
            }
        ]
    }
