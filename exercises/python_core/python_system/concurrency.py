import pandas as pd

def get_exercise():
    return {
        "title": "Concurrency",
        "subtitle": "Core python concepts",
        "description": """Two threads execute the worker function concurrently without a lock.\n\nWhich of the following is a possible final value for counter?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """\
import threading

counter = 0

def worker():
    global counter
    for _ in range(100_000):
        counter += 1

t1 = threading.Thread(target=worker)
t2 = threading.Thread(target=worker)
t1.start()
t2.start()
t1.join()
t2.join()
# print(counter)""",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = True # Concept exercise placeholder',
        "deep_dive": """The += operation is not atomic. It involves loading, adding, and storing. Because there is no thread lock, a context switch can occur mid-operation, causing race conditions where threads overwrite each other's increments. This results in \"lost updates,\" making a value less than 200,000 (like 150,000) the expected outcome.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """Two threads execute the worker function concurrently without a lock.\n\nWhich of the following is a possible final value for counter?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """200000""", "is_correct": False},
                     {"label": "B", "text": """150000""", "is_correct": True},
                     {"label": "C", "text": """0""", "is_correct": True},
                     {"label": "D", "text": """100000""", "is_correct": False},
                 ],
                 "explanation": """The += operation is not atomic. It involves loading, adding, and storing. Because there is no thread lock, a context switch can occur mid-operation, causing race conditions where threads overwrite each other's increments. This results in \"lost updates,\" making a value less than 200,000 (like 150,000) the expected outcome."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """Two threads execute the worker function concurrently without a lock.

Which of the following is a possible final value for counter?

""",
                "hint": "Return True to pass the concept check.",
                "data": """\
import threading

counter = 0

def worker():
    global counter
    for _ in range(100_000):
        counter += 1

t1 = threading.Thread(target=worker)
t2 = threading.Thread(target=worker)
t1.start()
t2.start()
t1.join()
t2.join()
# print(counter)""",
                "evaluation_criteria": ["Understanding of concept"],
                "solution_code": """\
result = True""",
                "expected_output": True,
                "big_o_explanation": "Constant time implementation.",
                "follow_up_probes": ["Can you explain the limitations?"]
            }
        ]
    }
