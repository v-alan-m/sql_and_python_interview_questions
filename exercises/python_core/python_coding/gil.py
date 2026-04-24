import pandas as pd

def get_exercise():
    return {
        "title": "The Global Interpreter Lock (GIL)",
        "subtitle": "GIL",
        "description": "Which of the given statements is true regarding Pythons Global Interpreter Lock (GIL)?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "Think about how Python handles multithreading. Does the GIL help or hinder performance when doing heavy mathematical computations (CPU-bound tasks) on a multi-core processor?",
        "solution_python": 'result = "The GIL is a limitation that affects the performance of CPU-bound multi-threaded programs."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

The Global Interpreter Lock (GIL) is one of the most controversial and misunderstood components of the default Python implementation (CPython). 

At its core, the GIL is a massive C-level mutex (lock) that protects access to Python objects. Because CPython's memory management (reference counting) is not thread-safe, the GIL ensures that only **one thread can execute Python bytecodes at any given time**, regardless of how many CPU cores your machine possesses.

This architectural decision has profound performance implications:
1. **CPU-bound tasks (e.g., number crunching, image processing):** If you spawn 4 threads to do heavy math on a 4-core processor, the GIL will force them to take turns running on a single core. The overhead of context switching actually makes the multi-threaded CPU-bound program *slower* than a single-threaded one. Thus, the GIL is a severe limitation here. To achieve true parallelism for CPU-bound tasks, developers must use the `multiprocessing` module, which spawns entirely separate OS processes (each with their own memory and GIL).
2. **I/O-bound tasks (e.g., network requests, file reading):** The GIL is intentionally released by the interpreter when a thread sits idle waiting for I/O. Therefore, multithreading *is* still highly effective for I/O-bound programs in Python.

- Option A is incorrect because the GIL actively prevents Python threads from efficiently utilizing multiple cores.
- Option B is incorrect because the GIL prevents race conditions at the *interpreter memory level*, not the *application level*. You still need `threading.Lock()` to protect your own data structures from race conditions.
- Option C is factually true in mechanics but does not capture the defining characteristic/statement posed in the correct answer regarding performance impact.""",
        "big_o_explanation": "O(1) - The GIL acts as a constant bottleneck, locking the interpreter state regardless of algorithmic complexity.",
        
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
                 "explanation": "The Global Interpreter Lock (GIL) is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at the same time. This bottlenecks CPU-bound multi-threaded programs, as only one thread can execute on a single core at any given time."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "The Global Interpreter Lock (GIL)",
                "scenario": "Which of the given statements is true regarding Pythons Global Interpreter Lock (GIL)?",
                "hint": "Think about how Python handles multithreading. Does the GIL help or hinder performance when doing heavy mathematical computations (CPU-bound tasks) on a multi-core processor?",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of Python's concurrency model", "Differentiating between CPU-bound and I/O-bound performance limitations caused by the GIL"],
                "solution_code": 'result = "The GIL is a limitation that affects the performance of CPU-bound multi-threaded programs."',
                "expected_output": 'The GIL is a limitation that affects the performance of CPU-bound multi-threaded programs.',
                "big_o_explanation": "O(1) - The GIL acts as a constant bottleneck, locking the interpreter state regardless of algorithmic complexity.",
                "follow_up_probes": ["Why didn't the creators of Python just remove the GIL entirely?", "How does the `multiprocessing` module bypass the GIL limitations?"]
            }
        ]
    }
