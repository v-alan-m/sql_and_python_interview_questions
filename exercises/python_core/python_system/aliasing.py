import pandas as pd

def get_exercise():
    return {
        "title": "Understanding Object Aliasing",
        "subtitle": "aliasing",
        "description": "Consider the following Python code:\n\n```python\nclass Sample:\n    def __init__(self):\n        self._data = []\n\n    def add_data(self, value):\n        self._data.append(value)\n\n    def get_data(self):\n        return self._data\n\nsample1 = Sample()\nsample2 = sample1\nsample1.add_data(10)\nsample2.add_data(20)\n```\n\nWhat will be the output of `print(sample1.get_data())`?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": pd.DataFrame({"id": [1, 2], "input": ["a", "b"]}),
        "allowed_modes": ["Python"],
        "hint_python": "Think about what happens in memory when you assign `sample2 = sample1`.",
        "solution_python": 'result = "[10, 20]"',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis question tests your understanding of object references and aliasing in Python.\n\n* **Assignment Operator:** In Python, the assignment operator `=` does not create a copy of the object. When executing `sample2 = sample1`, `sample2` simply becomes an alias for the exact same instance in memory that `sample1` refers to.\n* **Shared State:** Because both variables point to the same `Sample` object, they share the same internal `_data` list. \n* **Mutating Operations:** Calling `add_data(10)` via `sample1` appends `10` to this shared list. Subsequently, calling `add_data(20)` via `sample2` appends `20` to the same list. \n\nTherefore, accessing the list through either reference will yield `[10, 20]`.",
        "big_o_explanation": "O(1) - Appending to a list is an O(1) operation on average. Variable assignment simply copies the reference, which is also O(1).",

        # --- MULTICHOICE CONCEPTUAL QUESTIONS ---
        "mcq_questions": [
             {
                 "question": "What will be the output of `print(sample1.get_data())`?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "[10, 20]", "is_correct": True},
                     {"label": "B", "text": "[10]", "is_correct": False},
                     {"label": "C", "text": "[20]", "is_correct": False},
                     {"label": "D", "text": "None of the above", "is_correct": False},
                 ],
                 "explanation": "`sample2 = sample1` creates an alias, not a copy. Both variables point to the same object in memory. Appending to either modifies the shared list."
             }
        ],

        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "Consider the following Python code:\n\n```python\nclass Sample:\n    def __init__(self):\n        self._data = []\n\n    def add_data(self, value):\n        self._data.append(value)\n\n    def get_data(self):\n        return self._data\n\nsample1 = Sample()\nsample2 = sample1\nsample1.add_data(10)\nsample2.add_data(20)\n```\n\nWhat will be the output of `print(sample1.get_data())`?",
                "hint": "Think about what happens in memory when you assign `sample2 = sample1`.",
                "data": pd.DataFrame({"id": [1], "input": ["c"]}),
                "evaluation_criteria": ["Lead Engineer Concept 1", "Deep understanding of object references"],
                "solution_code": 'result = "[10, 20]"',
                "expected_output": '[10, 20]',
                "big_o_explanation": "O(1) - Modifying a shared list reference is O(1).",
                "follow_up_probes": ["How would you create a deep copy of the Sample object if needed?"]
            }
        ]
    }
