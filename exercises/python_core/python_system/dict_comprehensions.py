import pandas as pd

def get_exercise():
    return {
        "title": "Dictionary Comprehensions",
        "subtitle": "comprehensions",
        "description": "What is the content of new_dict after this dictionary comprehension runs?\n\n```python\nkeys = ['a', 'b', 'c', 'd']\nvalues = [1, 2, 3, 4]\nnew_dict = {k: v*v for k, v in zip(keys, values) if v % 2 == 0}\n```",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "First evaluate the `zip` pairing, then apply the `if` filter, and finally calculate the key-value mapping `k: v*v`.",
        "solution_python": 'result = "{''b'': 4, ''d'': 16}"',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis question evaluates your ability to trace complex data structure transformations using dictionary comprehensions.\n\n* **Zipping:** The `zip(keys, values)` function lazily aggregates the lists into tuples: `('a', 1), ('b', 2), ('c', 3), ('d', 4)`.\n* **Filtering:** The condition `if v % 2 == 0` filters the tuples, keeping only those where the value is even. This discards `'a'` and `'c'`, leaving `('b', 2)` and `('d', 4)`.\n* **Mapping:** The expression `k: v*v` determines the final output structure. For `'b'`, the value `2` is squared to `4`. For `'d'`, the value `4` is squared to `16`.\n\nCombining these operations yields `{'b': 4, 'd': 16}`. Dictionary comprehensions are highly preferred over initializing an empty `dict()` and running a `for` loop, as they are both more readable and performant.",
        "big_o_explanation": "O(n) - A single pass over the lists of length n.",
        "mcq_questions": [
             {
                 "question": "What is the content of new_dict after this dictionary comprehension runs?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "{'a': 1, 'b': 4, 'c': 9, 'd': 16}", "is_correct": False},
                     {"label": "B", "text": "{'b': 4, 'd': 16}", "is_correct": True},
                     {"label": "C", "text": "{'b': 2, 'd': 4}", "is_correct": False},
                     {"label": "D", "text": "{'a': 1, 'c': 9}", "is_correct": False},
                 ],
                 "explanation": "zip(keys, values) pairs the lists: ('a',1), ('b',2), ('c',3), ('d',4). The filter 'if v % 2 == 0' keeps only even values (b=2, d=4). The mapping 'k: v*v' squares the values. So 'b' maps to 4, and 'd' maps to 16, resulting in {'b': 4, 'd': 16}."
             }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "What is the content of new_dict after this dictionary comprehension runs?\n\n```python\nkeys = ['a', 'b', 'c', 'd']\nvalues = [1, 2, 3, 4]\nnew_dict = {k: v*v for k, v in zip(keys, values) if v % 2 == 0}\n```",
                "hint": "First evaluate the `zip` pairing, then apply the `if` filter, and finally calculate the key-value mapping `k: v*v`.",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of dict comprehensions", "Understanding of zip behavior"],
                "solution_code": 'result = "{''b'': 4, ''d'': 16}"',
                "expected_output": '{\'b\': 4, \'d\': 16}',
                "big_o_explanation": "O(n) - Iterates through both lists simultaneously.",
                "follow_up_probes": ["How would you structure this using a traditional loop? Is the time complexity different?"]
            }
        ]
    }
