import pandas as pd

def get_exercise():
    return {
        "title": "The Global Interpreter Lock (GIL)",
        "subtitle": "threading",
        "description": "Which of the given statements is true regarding Pythons Global Interpreter Lock (GIL)?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "Think about the main criticism of Python's threading model when dealing with heavy CPU tasks.",
        "solution_python": 'result = "The GIL is a limitation that affects the performance of CPU-bound multi-threaded programs."',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis question probes a fundamental architectural constraint of the standard Python implementation (CPython).\n\n* **What is the GIL?** The Global Interpreter Lock is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once.\n* **The Impact on CPU-Bound Tasks:** For pure computational tasks (like image processing or math calculations), multithreading in Python does not provide true parallelism. The threads will just take turns holding the GIL, and the overhead of context switching can actually make a multi-threaded CPU-bound program slower than a single-threaded one.\n* **When Threads Work in Python:** The GIL *is* released during I/O operations (like network requests or file reads). Thus, Python threads are highly effective for I/O-bound tasks where threads spend most of their time waiting for external responses.\n\nTo achieve true parallelism for CPU-bound tasks in Python, you must use the `multiprocessing` module, which creates separate processes, each with its own Python interpreter and its own GIL.",
        "big_o_explanation": "N/A - This is an architectural limitation, not an algorithmic complexity.",
        "mcq_questions": [
             {
                 "question": "Which of the given statements is true regarding Pythons Global Interpreter Lock (GIL)?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "The GIL allows Python to efficiently utilize multi-core processors.", "is_correct": False},
                     {"label": "B", "text": "The GIL is a feature designed to prevent race conditions in multi-threaded programs.", "is_correct": False},
                     {"label": "C", "text": "The GIL is released whenever I/O-bound operations are performed.", "is_correct": False},
                     {"label": "D", "text": "The GIL is a limitation that affects the performance of CPU-bound multi-threaded programs.", "is_correct": True},
                 ],
                 "explanation": "The GIL is a mutex that allows only one thread to hold control of the Python interpreter. This drastically limits parallel execution for CPU-bound tasks. While option C is also technically true contextually, option D highlights the fundamental architectural limitation evaluated here."
             }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "Which of the given statements is true regarding Pythons Global Interpreter Lock (GIL)?",
                "hint": "Think about the main criticism of Python's threading model when dealing with heavy CPU tasks.",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of Python's GIL constraint", "Knowledge of CPU-bound vs I/O-bound limits"],
                "solution_code": 'result = "The GIL is a limitation that affects the performance of CPU-bound multi-threaded programs."',
                "expected_output": 'The GIL is a limitation that affects the performance of CPU-bound multi-threaded programs.',
                "big_o_explanation": "N/A - Architectural limitation.",
                "follow_up_probes": ["What module would you use instead of threading to achieve true parallelism for CPU-bound tasks?"]
            }
        ]
    }
