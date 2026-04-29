import pandas as pd

def get_exercise():
    return {
        "title": "Custom Iterators and Magic Methods",
        "subtitle": "iterators",
        "description": "Consider the following Python code:\nWhat will be the value of the result after executing the above code?",
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
        "hint_python": "Walk through the `__next__` method calls. What values are yielded before `self.current` hits or exceeds the `limit` of 10?",
        "solution_python": "result = 30",
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

To build an iterator in Python, an object must adhere to the Iterator Protocol by implementing two magic methods:
1. `__iter__(self)`: Must return the iterator object itself. This makes the object compatible with `for` loops, comprehensions, and functions like `sum()`.
2. `__next__(self)`: Must return the next item in the sequence. When the sequence is exhausted, it must raise a `StopIteration` exception.

When the built-in `sum()` function receives the `numbers` object, it implicitly calls `iter(numbers)` (which triggers `__iter__`) and then repeatedly calls `next(numbers)` (which triggers `__next__`) until `StopIteration` is raised.

Let's trace the state of `self.current`:
- Initial state: `self.current = 0`
- 1st `__next__` call: `0 < 10`, increments to `2`, returns `2`.
- 2nd `__next__` call: `2 < 10`, increments to `4`, returns `4`.
- 3rd `__next__` call: `4 < 10`, increments to `6`, returns `6`.
- 4th `__next__` call: `6 < 10`, increments to `8`, returns `8`.
- 5th `__next__` call: `8 < 10`, increments to `10`, returns `10`.
- 6th `__next__` call: `10 >= 10`, raises `StopIteration`.

The sequence yielded is `[2, 4, 6, 8, 10]`.
The `sum()` function accumulates these values: `2 + 4 + 6 + 8 + 10 = 30`.

- Option A (20) is incorrect; it misses the last two items.
- Option B (25) is incorrect; it assumes odd numbers or a different step.
- Option D (35) is incorrect; it includes a value past the limit.""",
        "big_o_explanation": "O(N) - The iterator must generate N elements linearly up to the limit, and `sum` processes them in O(N) time.",
        
        "mcq_questions": [
             {
                 "question": "What will be the value of the result after executing the custom iterator code?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "20", "is_correct": False},
                     {"label": "B", "text": "25", "is_correct": False},
                     {"label": "C", "text": "30", "is_correct": True},
                     {"label": "D", "text": "35", "is_correct": False},
                 ],
                 "explanation": "This code implements a custom iterator using Python's magic methods `__iter__` and `__next__`. When `sum(numbers)` is called, it repeatedly calls `__next__()` until a `StopIteration` exception is raised. The sequence yielded is 2, 4, 6, 8, 10. The sum of these values is 30."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Custom Iterators and Magic Methods",
                "scenario": "Consider the following Python code:\nWhat will be the value of the result after executing the above code?",
                "hint": "Walk through the `__next__` method calls. What values are yielded before `self.current` hits or exceeds the `limit` of 10?",
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
                "evaluation_criteria": ["Understanding of the Iterator Protocol (__iter__, __next__)", "Tracing state mutations across repeated method calls"],
                "solution_code": "result = 30",
                "expected_output": 30,
                "big_o_explanation": "O(N) - The iterator must generate N elements linearly up to the limit, and `sum` processes them in O(N) time.",
                "follow_up_probes": ["How could you rewrite this custom class using a generator function (`yield`)?", "Why does Python require `__iter__` to return `self` for iterators?"]
            }
        ]
    }
