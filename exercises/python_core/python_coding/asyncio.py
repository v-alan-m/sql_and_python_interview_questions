import pandas as pd

def get_exercise():
    return {
        "title": "Asyncio Execution Model",
        "subtitle": "asyncio",
        "description": "Consider an asynchronous Python script handling API requests using asyncio. When the interpreter encounters an `await` expression (e.g., `await fetch_data()`), what happens behind the scenes at the system level?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": None,
        "hide_data": True,
        "allowed_modes": ["Python"],
        "hint_python": "Think about how asyncio differs from multi-threading. Does it spawn new OS threads, or does it multiplex within a single thread?",
        "solution_python": 'result = "The function yields control back to the event loop, suspending its state and allowing the event loop to run other scheduled coroutines while waiting for the I/O to finish."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

Python's `asyncio` implements **cooperative multitasking** primarily within a single thread. This is a fundamentally different concurrency model compared to multi-threading or multi-processing. 

When the interpreter encounters the `await` keyword, it acts as a yield point. Instead of blocking the entire thread (which would freeze the application) or spawning an OS-level thread (which incurs heavy context-switching overhead and GIL contention), the coroutine effectively says: *"I'm going to wait for an I/O operation to complete. Here is my current state; pause me and let someone else run."*

Control is immediately handed back to the **Event Loop**. The event loop then looks at its queue of scheduled tasks and resumes the next ready coroutine. Once the underlying non-blocking I/O operation signals completion (via OS-level multiplexing primitives like `epoll` or `kqueue`), the event loop wakes the suspended coroutine back up to resume execution precisely where it left off.

- Option A describes synchronous, blocking execution, which is exactly what `asyncio` aims to avoid.
- Option B incorrectly suggests OS threads are used. `asyncio` is single-threaded by design.
- Option D incorrectly suggests OS-level interrupts are used to force prioritization, which is not how the user-space event loop operates.""",
        "big_o_explanation": "O(1) - Context switching between coroutines in the event loop is heavily optimized and generally operates in constant time per task switch, avoiding expensive OS-level thread context switches.",
        
        "mcq_questions": [
             {
                 "question": "Consider an asynchronous Python script handling API requests using asyncio. When the interpreter encounters an await expression (e.g., `await fetch_data()`), what happens behind the scenes at the system level?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "The current thread is blocked entirely until the I/O operation completes, mimicking synchronous execution.", "is_correct": False},
                     {"label": "B", "text": "A new thread is instantly spawned to handle the I/O request to bypass the Global Interpreter Lock (GIL).", "is_correct": False},
                     {"label": "C", "text": "The function yields control back to the event loop, suspending its state and allowing the event loop to run other scheduled coroutines while waiting for the I/O to finish.", "is_correct": True},
                     {"label": "D", "text": "The function triggers an immediate interrupt signal at the OS level to force I/O prioritization.", "is_correct": False},
                 ],
                 "explanation": "asyncio uses cooperative multitasking within a single thread. The await keyword acts similarly to a yield point. It pauses the coroutine, preserves its execution state, and hands control back to the event loop. This enables the single thread to remain active, executing other tasks while waiting for non-blocking I/O operations to complete."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Asyncio Execution Model",
                "scenario": "Consider an asynchronous Python script handling API requests using asyncio. When the interpreter encounters an `await` expression (e.g., `await fetch_data()`), what happens behind the scenes at the system level?",
                "hint": "Think about how asyncio differs from multi-threading. Does it spawn new OS threads, or does it multiplex within a single thread?",
                "data": None,
                "hide_data": True,
                "evaluation_criteria": ["Understanding of event loops", "Differentiating cooperative multitasking from threading"],
                "solution_code": 'result = "The function yields control back to the event loop, suspending its state and allowing the event loop to run other scheduled coroutines while waiting for the I/O to finish."',
                "expected_output": 'The function yields control back to the event loop, suspending its state and allowing the event loop to run other scheduled coroutines while waiting for the I/O to finish.',
                "big_o_explanation": "O(1) - Context switching between coroutines in the event loop is heavily optimized and generally operates in constant time per task switch, avoiding expensive OS-level thread context switches.",
                "follow_up_probes": ["What happens if you accidentally write a blocking `time.sleep()` call inside a coroutine?", "How do you run blocking CPU-bound code within an asyncio application?"]
            }
        ]
    }
