import pandas as pd

def get_exercise():
    return {
        "title": "Generators",
        "subtitle": "Core python concepts",
        "description": """What is the output of the following script that uses a generator function?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """\
def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count += 1

counter = count_up_to(3)
next(counter)
print(next(counter))""",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = 2',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**
This question tests your understanding of Python generators, specifically how they manage state and implement lazy evaluation using the `yield` keyword. As a Lead Engineer, understanding how to leverage generators for memory-efficient data processing is essential.

Here is the step-by-step execution breakdown:

* **Generator Initialization:** `counter = count_up_to(3)` does *not* execute the function body. Instead, it creates a generator object and assigns it to the variable `counter`.
* **First `next()` Call:** The standalone `next(counter)` statement triggers the execution of the generator body. It yields `1`, and the generator's state is now suspended at this exact line. The yielded value `1` is discarded because it wasn't assigned or printed.
* **Second `next()` Call:** The statement `print(next(counter))` evaluates the inner `next(counter)` first. 
    * The generator resumes execution immediately *after* the previous `yield` statement.
    * It updates the local variable to `2`.
    * The function hits `yield` again, yielding `2`, and suspends its state once more.
* **The Output:** The value `2` returned by the second `next()` call is passed directly to the `print()` function, outputting `2` to the console.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """What is the output of the following script that uses a generator function?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """1""", "is_correct": False},
                     {"label": "B", "text": """3""", "is_correct": False},
                     {"label": "C", "text": """2""", "is_correct": True},
                     {"label": "D", "text": """A StopIteration exception is raised.""", "is_correct": False},
                 ],
                 "explanation": """The first next() call executes until the first yield, returning 1 and suspending state. The second next() call resumes, increments count to 2, and yields 2. The print function receives and outputs this 2."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """What is the output of the following script that uses a generator function?

""",
                "hint": "Evaluate how the 'yield' keyword suspends a function's execution state, and how 'next()' resumes it.",
                "data": """\
def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count += 1

counter = count_up_to(3)
next(counter)
print(next(counter))""",
                "evaluation_criteria": ["Understanding of lazy evaluation", "Knowledge of generator state retention", "Memory optimization principles"],
                "solution_code": 'result = 2',
                "expected_output": 2,
                "big_o_explanation": "O(1) Space Complexity. A generator yields one item at a time, preventing memory exhaustion even for infinite sequences.",
                "follow_up_probes": ["How do generators differ from standard iterators that implement __iter__ and __next__?", "How would you chain multiple generators together for a data pipeline?"]
            }
        ]
    }
