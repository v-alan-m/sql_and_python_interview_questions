import pandas as pd

def get_exercise():
    return {
        "title": "Data Structures",
        "subtitle": "Data Structures",
        "description": """What is the primary performance benefit of using a set instead of a list to check for the existence of an item?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": "No specific code setup required for this conceptual problem.",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = "Sets use hash tables, providing average O(1) time for membership testing."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**
This question strikes at the core of understanding Python's underlying data structures and their algorithmic complexities. For a Lead Python Engineer, algorithmic efficiency is paramount when processing large datasets.

Here is the technical breakdown of why this is correct:

* **The Underlying Data Structure:** Python's `set` is implemented using a hash table (similar to the keys in a `dict`). When you check for membership using the `in` operator (`if item in my_set`), Python calculates the hash of the item and immediately jumps to the corresponding bucket in memory. 
* **Time Complexity:** Because of this hashing mechanism, the average time complexity for a lookup in a set is $O(1)$ (constant time). Regardless of whether the set has 10 elements or 10 million elements, the lookup time remains roughly the same.
* **Contrast with Lists:** A `list` is a dynamic array. To determine if an item exists in an unsorted list, Python must perform a linear scan, checking each element one by one. The average and worst-case time complexity for this is $O(n)$, where $n$ is the number of elements. 

While sets consume slightly more memory due to hash table overhead (sparse arrays to minimize collisions), the exponential speedup in lookups makes them indispensable for deduplication and membership checking.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """What is the primary performance benefit of using a set instead of a list to check for the existence of an item?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """Sets consume significantly less memory for the same number of elements.""", "is_correct": False},
                     {"label": "B", "text": """Sets use hash tables, providing average O(1) time for membership testing.""", "is_correct": True},
                     {"label": "C", "text": """Sets maintain their elements in a sorted order, which allows for faster binary searching.""", "is_correct": False},
                     {"label": "D", "text": """Lists require a linear scan, which has a best-case time complexity of O(n).""", "is_correct": False},
                 ],
                 "explanation": """Sets are implemented using hash tables, allowing Python to calculate a hash and immediately jump to the memory bucket for an average O(1) constant time lookup. Lists require an O(n) linear scan on average. Sets actually consume more memory than lists due to hash table overhead."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """What is the primary performance benefit of using a set instead of a list to check for the existence of an item?

""",
                "hint": "Think about how Python sets are implemented under the hood. Do they rely on contiguous memory arrays, or something else?",
                "data": "No specific code setup required for this conceptual problem.",
                "evaluation_criteria": ["Knowledge of internal memory structures (Hash Tables vs Arrays)", "Time complexity analysis capabilities", "Trade-off evaluation (Time vs Memory)"],
                "solution_code": 'result = "Sets use hash tables, providing average O(1) time for membership testing."',
                "expected_output": "Sets use hash tables, providing average O(1) time for membership testing.",
                "big_o_explanation": "O(1) Time on average for lookups. O(N) Space due to the underlying hash table allocation.",
                "follow_up_probes": ["What happens to the O(1) time complexity if there are massive hash collisions?", "Why can't you put a dictionary inside a set?"]
            }
        ]
    }
