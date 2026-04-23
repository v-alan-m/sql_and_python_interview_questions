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
        "solution_python": 'result = 150000',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**
This question is designed to test your knowledge of **race conditions** and the limits of Python's GIL. Here is the architectural breakdown of why the counter will likely "lose" updates and land somewhere around 150,000 instead of a perfect 200,000:

* **The Myth of the GIL:** Many developers mistakenly believe that because CPython has a Global Interpreter Lock, their Python code is inherently thread-safe. The GIL protects Python's *internal memory management*, not your application-level data.
* **Non-Atomic Operations:** The core issue lies in the line `counter += 1`. In Python, this is **not an atomic operation**. If you inspect this with Python's `dis` (disassembler) module, you'll see it breaks down into several bytecode instructions:
    1.  `LOAD_GLOBAL` (read the current value of `counter`)
    2.  `LOAD_CONST` (load the value `1`)
    3.  `INPLACE_ADD` (add the two values together)
    4.  `STORE_GLOBAL` (write the new value back to memory)
* **The Context Switch (Race Condition):** The GIL forces threads to take turns executing these bytecodes. A thread context switch can easily happen right in the middle of these steps. Both threads might read `100`, add `1`, and independently store `101`, resulting in one lost update.

Because this code runs 100,000 times concurrently without a `threading.Lock()` to synchronize the `counter += 1` operation, thousands of these updates will inevitably collide and be lost.""",
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
                "hint": "Remember that CPython's GIL protects internal memory, but does it protect application-level operations like '+=' from race conditions?",
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
                "evaluation_criteria": ["Understanding of atomic vs non-atomic operations", "Demystification of the GIL", "Identification of race conditions"],
                "solution_code": 'result = 150000',
                "expected_output": 150000,
                "big_o_explanation": "O(N) Time per thread where N is the loop count. O(1) Space.",
                "follow_up_probes": ["How would you rewrite this code to be perfectly thread-safe?", "If the operation was list.append() instead of += 1, would you still lose data?"]
            }
        ]
    }
