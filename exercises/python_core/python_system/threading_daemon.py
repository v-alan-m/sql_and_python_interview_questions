import pandas as pd

def get_exercise():
    return {
        "title": "Daemon Threads",
        "subtitle": "threading",
        "description": "In Python's threading module, what is the primary consequence of setting a thread as a \"daemon\" thread?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": pd.DataFrame({"id": [1, 2], "input": ["a", "b"]}),
        "allowed_modes": ["Python"],
        "hint_python": "Consider what happens to the main program when all non-daemon threads have finished executing.",
        "solution_python": 'result = "The program will exit even if the daemon thread is still running."',
        "deep_dive": "**Why this is correct (Lead Engineer Perspective):**\nThis question evaluates your knowledge of thread lifecycle management in Python.\n\n* **The Interpreter Lifespan:** By design, the Python interpreter remains alive and active as long as there is at least one non-daemon thread (including the main thread) actively running.\n* **The Role of Daemon Threads:** Setting `daemon=True` on a thread explicitly flags it as a background utility task (e.g., a background garbage collector, a heartbeat monitor, or a background cache refresher). \n* **Forceful Termination:** Once the main thread and all other standard threads conclude their execution, Python will not wait for daemon threads to finish. It will forcefully terminate them and exit the program immediately. \n\nUnderstanding this distinction is critical; if you spawn a thread to write critical data to a database and accidentally flag it as a daemon, the program might exit before the write completes, leading to data loss.",
        "big_o_explanation": "N/A - This is a concurrency lifecycle concept.",
        "mcq_questions": [
             {
                 "question": "In Python's threading module, what is the primary consequence of setting a thread as a \"daemon\" thread?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "The daemon thread is given a higher execution priority over non-daemon threads.", "is_correct": False},
                     {"label": "B", "text": "The program will exit even if the daemon thread is still running.", "is_correct": True},
                     {"label": "C", "text": "The daemon thread is not allowed to access any global variables.", "is_correct": False},
                     {"label": "D", "text": "The daemon thread runs in the background and cannot be manually joined.", "is_correct": False},
                 ],
                 "explanation": "In Python, the entire Python program (the interpreter) stays alive as long as there is at least one non-daemon thread actively running. When you set daemon=True on a thread, you are explicitly telling Python: 'This is a background utility task. Do not wait for it to finish.' Once the main thread and all other non-daemon threads complete their execution, the Python interpreter will forcefully terminate any remaining daemon threads and exit."
             }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": "In Python's threading module, what is the primary consequence of setting a thread as a \"daemon\" thread?",
                "hint": "Consider what happens to the main program when all non-daemon threads have finished executing.",
                "data": pd.DataFrame({"id": [1], "input": ["c"]}),
                "evaluation_criteria": ["Understanding of daemon threads", "Knowledge of interpreter lifecycle"],
                "solution_code": 'result = "The program will exit even if the daemon thread is still running."',
                "expected_output": 'The program will exit even if the daemon thread is still running.',
                "big_o_explanation": "N/A",
                "follow_up_probes": ["Can you `join()` a daemon thread? What happens if you do?"]
            }
        ]
    }
