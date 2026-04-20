import pandas as pd

def get_exercise():
    return {
        "title": "Asyncio",
        "subtitle": "Core python concepts",
        "description": """Consider an asynchronous Python script handling API requests using asyncio. When the interpreter encounters an await expression (e.g., `await fetch_data()`), what happens behind the scenes at the system level?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": "No specific code setup required for this conceptual problem.",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = True # Concept exercise placeholder',
        "deep_dive": """asyncio uses cooperative multitasking within a single thread. The await keyword acts similarly to a yield point. It pauses the coroutine, preserves its execution state, and hands control back to the event loop. This enables the single thread to remain active, executing other tasks while waiting for non-blocking I/O operations to complete.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """Consider an asynchronous Python script handling API requests using asyncio. When the interpreter encounters an await expression (e.g., `await fetch_data()`), what happens behind the scenes at the system level?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """The current thread is blocked entirely until the I/O operation completes, mimicking synchronous execution.""", "is_correct": False},
                     {"label": "B", "text": """A new thread is instantly spawned to handle the I/O request to bypass the Global Interpreter Lock (GIL).""", "is_correct": False},
                     {"label": "C", "text": """The function yields control back to the event loop, suspending its state and allowing the event loop to run other scheduled coroutines while waiting for the I/O to finish.""", "is_correct": True},
                     {"label": "D", "text": """The function triggers an immediate interrupt signal at the OS level to force I/O prioritization.""", "is_correct": False},
                 ],
                 "explanation": """asyncio uses cooperative multitasking within a single thread. The await keyword acts similarly to a yield point. It pauses the coroutine, preserves its execution state, and hands control back to the event loop. This enables the single thread to remain active, executing other tasks while waiting for non-blocking I/O operations to complete."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """Consider an asynchronous Python script handling API requests using asyncio. When the interpreter encounters an await expression (e.g., `await fetch_data()`), what happens behind the scenes at the system level?

""",
                "hint": "Return True to pass the concept check.",
                "data": "No specific code setup required for this conceptual problem.",
                "evaluation_criteria": ["Understanding of concept"],
                "solution_code": """\
result = True""",
                "expected_output": True,
                "big_o_explanation": "Constant time implementation.",
                "follow_up_probes": ["Can you explain the limitations?"]
            }
        ]
    }
