import pandas as pd

def get_exercise():
    return {
        "title": "Sorting Objects/Dictionaries (10/10)",
        "subtitle": "Arrays / Lists",
        "description": "You are given a DataFrame column 'user_records' containing Python dictionaries. Sort this list of JSON-like objects FIRST by 'department' in ascending alphabetical order, and THEN by 'salary' in descending order. Return the sorted list.",
        "data": pd.DataFrame({"user_records": [
            {"id": 1, "department": "Engineering", "salary": 120000},
            {"id": 2, "department": "Sales", "salary": 85000},
            {"id": 3, "department": "Engineering", "salary": 140000},
            {"id": 4, "department": "Sales", "salary": 95000},
            {"id": 5, "department": "HR", "salary": 75000}
        ]}),
        "allowed_modes": ["Python"],
        "hint_python": "Use Python's built-in `.sort()` method or `sorted()` function with a custom `key` argument using a `lambda`. To sort descending by salary, you can negate the integer value (-salary) in the tuple returned by the lambda.",
        "solution_python": """def sort_objects(records):
    # Sort by department (asc), then by salary (descending via negation)
    return sorted(records, key=lambda x: (x['department'], -x['salary']))

records = df['user_records'].tolist()
result = sort_objects(records)
""",
        "deep_dive": "In real-world data engineering, you rarely sort raw integers. Most times, data arrives as JSON payloads from APIs or rows from a NoSQL database. Mastering `lambda` sort keys and multi-level sorting logic in Python is a crucial daily skill."
    }
