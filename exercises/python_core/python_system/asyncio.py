import pandas as pd

def get_exercise():
    return {
        "title": "Asyncio",
        "subtitle": "Asyncio",
        "description": """Consider an asynchronous Python script handling API requests using asyncio. When the interpreter encounters an await expression (e.g., `await fetch_data()`), what happens behind the scenes at the system level?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": "No specific code required.",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": """result = "The function yields control back to the event loop, suspending its state and allowing the event loop to run other scheduled coroutines while waiting for the I/O to finish." """,
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**
This question tests your architectural understanding of Python's asynchronous I/O model. As a lead engineer, choosing between multi-threading, multi-processing, or asyncio dictates the scalability of your entire backend.

1. **Cooperative Multitasking:** Unlike OS-level threads where the operating system forcibly pauses threads (preemptive multitasking), `asyncio` uses *cooperative* multitasking. The coroutines themselves must explicitly declare when they are ready to pause.
2. **The Yield Point:** The `await` keyword is that declaration. It acts similarly to a `yield` in a generator. When the interpreter hits `await fetch_data()`, the current coroutine is suspended, its local state is preserved, and control is explicitly handed back to the central Event Loop.
3. **Concurrency on a Single Thread:** Because control was returned, the single OS thread is not blocked waiting for the network response. The Event Loop immediately switches to executing other queued coroutines. 
4. **Resumption:** Once the OS signals that the I/O for `fetch_data()` is ready, the Event Loop schedules the original coroutine to resume exactly where it left off.

This model allows a single Python thread to handle tens of thousands of concurrent network connections, massively outperforming standard threading for I/O bound workloads.""",
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
                "hint": "Asyncio runs on a single thread. How does it manage to handle multiple network requests concurrently without blocking?",
                "data": "No specific code required.",
                "evaluation_criteria": ["Deep understanding of Event Loops and Cooperative Multitasking", "Differentiating Asyncio from Multithreading", "Scalability architecture"],
                "solution_code": """result = "The function yields control back to the event loop, suspending its state and allowing the event loop to run other scheduled coroutines while waiting for the I/O to finish." """,
                "expected_output": "The function yields control back to the event loop, suspending its state and allowing the event loop to run other scheduled coroutines while waiting for the I/O to finish.",
                "big_o_explanation": "O(1) Context Switch Time. Switching between coroutines is vastly cheaper than switching OS-level threads.",
                "follow_up_probes": ["What happens if you run a heavy CPU-bound calculation (like computing primes) inside an async function?", "How do you safely mix synchronous legacy code with asyncio?"]
            }
        ]
    }
