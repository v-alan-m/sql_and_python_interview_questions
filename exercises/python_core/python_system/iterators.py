import pandas as pd

def get_exercise():
    return {
        "title": "Custom Iterators and the Iteration Protocol",
        "subtitle": "iterators",
        "description": "Consider the following Python code:\n\nWhat will be the value of the result after executing the above code?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """class CustomIterator:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        else:
            self.current += 2
            return self.current

    def __iter__(self):
        return self

numbers = CustomIterator(10)
result = sum(numbers)""",
        "hide_data": False,
        "allowed_modes": ["Python"],
        "hint_python": "Trace the values yielded by `__next__` until `StopIteration` is raised.",
        "solution_python": 'result = 30',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis question evaluates your understanding of Python's iterator protocol, specifically the `__iter__` and `__next__` dunder methods.\n\n* **Iterator State:** `self.current` starts at 0. \n* **The `__next__` Loop:** Each call to `__next__` increments `self.current` by 2 *before* returning it. The yielded sequence is 2, 4, 6, 8, 10.\n* **Stop Condition:** Once `self.current` reaches `10`, the next iteration checks `if self.current >= self.limit:` (`10 >= 10`), which evaluates to `True`, raising `StopIteration`.\n* **Consumption:** The `sum()` function implicitly handles `StopIteration`, catching it to stop aggregating. `2 + 4 + 6 + 8 + 10 = 30`.\n\nIterators are incredibly powerful for managing memory when working with large data streams, generating items on the fly instead of loading everything into a list.",
        "big_o_explanation": "O(n) - The iterator yields n/2 items, which the sum function aggregates in linear time.",
        "mcq_questions": [
             {
                 "question": "What will be the value of the result after executing the above code?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "20", "is_correct": False},
                     {"label": "B", "text": "25", "is_correct": False},
                     {"label": "C", "text": "30", "is_correct": True},
                     {"label": "D", "text": "35", "is_correct": False},
                 ],
                 "explanation": "The custom iterator implements `__iter__` and `__next__`. It starts at 0, increments by 2, and yields values until current reaches 10 (yielding 2, 4, 6, 8, 10). The sum() function consumes the iterator and totals the yielded values: 2+4+6+8+10 = 30."
             }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "Consider the following Python code:\n\nWhat will be the value of the result after executing the above code?",
                "hint": "Trace the values yielded by `__next__` until `StopIteration` is raised.",
                "data": """class CustomIterator:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        else:
            self.current += 2
            return self.current

    def __iter__(self):
        return self

numbers = CustomIterator(10)
result = sum(numbers)""",
                "hide_data": False,
                "evaluation_criteria": ["Understanding of python iterators", "Tracing program state changes"],
                "solution_code": 'result = 30',
                "expected_output": 30,
                "big_o_explanation": "O(n) - Iterates linearly based on the limit.",
                "follow_up_probes": ["Could you implement the exact same logic using a generator instead of a class?"]
            }
        ]
    }
