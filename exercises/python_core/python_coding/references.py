import pandas as pd

def get_exercise():
    return {
        "title": "Object References and Mutability",
        "subtitle": "references",
        "description": "Consider the following Python code:\nWhat will be the output of `print(sample1.get_data())`?\n\n```python\nclass Sample:\n    def __init__(self):\n        self._data = []\n\n    def add_data(self, value):\n        self._data.append(value)\n\n    def get_data(self):\n        return self._data\n\nsample1 = Sample()\nsample2 = sample1\nsample1.add_data(10)\nsample2.add_data(20)\n```",
        "difficulty_level": "easy",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "When you assign `sample2 = sample1`, are you creating a brand new object, or are you creating an alias (a new name tag) pointing to the exact same object in memory?",
        "solution_python": "result = [10, 20]",
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

A fundamental concept in Python is that variables are not buckets that hold data; they are **labels (references)** pointing to objects in memory.

When the line `sample1 = Sample()` executes, Python allocates memory for a new `Sample` instance on the heap and creates a label named `sample1` that points to it. This instance initializes an empty list `_data = []`.

When the line `sample2 = sample1` executes, Python **does not** create a copy of the `Sample` object. Instead, it creates a second label, `sample2`, and attaches it to the exact same object in memory that `sample1` is pointing to. 

This is known as **aliasing**. Because `sample1` and `sample2` point to the identical instance:
1. `sample1.add_data(10)` accesses the instance's `_data` list and appends `10`. The list is now `[10]`.
2. `sample2.add_data(20)` accesses the *same instance's* `_data` list and appends `20`. The list is now `[10, 20]`.

Since both variables operate on the same shared state, calling `sample1.get_data()` returns the fully modified list `[10, 20]`.

- Option B ([10]) is incorrect because it implies `sample2` modified a different object.
- Option C ([20]) is incorrect because it implies `sample1` modifications were overwritten or isolated.
- Option D (None of the above) is incorrect as the behavior is completely deterministic.""",
        "big_o_explanation": "O(1) - Reference assignment and list appends are constant-time operations.",
        
        "mcq_questions": [
             {
                 "question": "What will be the output of print(sample1.get_data())?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "[10, 20]", "is_correct": True},
                     {"label": "B", "text": "[10]", "is_correct": False},
                     {"label": "C", "text": "[20]", "is_correct": False},
                     {"label": "D", "text": "None of the above", "is_correct": False},
                 ],
                 "explanation": "When `sample2 = sample1` executes, it creates a new reference to the exact same object in memory, not a copy. Any modifications made through `sample1` or `sample2` affect the shared `_data` list. Therefore, both 10 and 20 are appended to the same list."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Object References and Mutability",
                "scenario": "Consider the following Python code:\nWhat will be the output of `print(sample1.get_data())`?\n\n```python\nclass Sample:\n    def __init__(self):\n        self._data = []\n\n    def add_data(self, value):\n        self._data.append(value)\n\n    def get_data(self):\n        return self._data\n\nsample1 = Sample()\nsample2 = sample1\nsample1.add_data(10)\nsample2.add_data(20)\n```",
                "hint": "When you assign `sample2 = sample1`, are you creating a brand new object, or are you creating an alias (a new name tag) pointing to the exact same object in memory?",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of object references vs deep copies", "Recognizing side effects on mutable shared state"],
                "solution_code": "result = [10, 20]",
                "expected_output": [10, 20],
                "big_o_explanation": "O(1) - Reference assignment and list appends are constant-time operations.",
                "follow_up_probes": ["How would you rewrite this code to ensure `sample2` gets an independent copy of the object?", "Does `copy.copy()` create an independent copy of `_data` inside the class?"]
            }
        ]
    }
