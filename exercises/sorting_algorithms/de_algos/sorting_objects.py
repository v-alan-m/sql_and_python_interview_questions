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
        "deep_dive": "In real-world data engineering, you rarely sort raw integers. Most times, data arrives as JSON payloads from APIs or rows from a NoSQL database. Mastering `lambda` sort keys and multi-level sorting logic in Python is a crucial daily skill.",
        "big_o_explanation": "### Time Complexity: $O(N \\log N)$\nWhere **$N$** is the number of objects (dictionaries) in the list.\n- Python's built-in `sorted()` function leverages the **Timsort** algorithm, which is a hybrid of Merge Sort and Insertion Sort.\n- Timsort guarantees a worst-case and average-case time complexity of $O(N \\log N)$.\n- The custom `lambda` key simply extracts properties from each object in $O(1)$ time per comparison, so it does not increase the overall asymptotic time bound.\n\n### Space Complexity: $O(N)$\n- Timsort requires $O(N)$ auxiliary space in the worst case to perform its merge operations.\n- Additionally, creating the new sorted list to return takes $O(N)$ space.\n\n### Optimization Context\nUsing a native, highly-optimized sorting algorithm like Timsort (via `sorted()` or `.sort()`) is vastly superior to writing a custom sort function in raw Python. Furthermore, using a `lambda` tuple `(x['department'], -x['salary'])` allows you to execute a complex multi-stage sort in a single pass of the sorting algorithm, rather than having to sort the data multiple times. The negation trick (`-x['salary']`) is an elegant $O(1)$ optimization to mix ascending and descending sorts simultaneously."
    }
