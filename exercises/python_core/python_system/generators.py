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
        "solution_python": 'result = True # Concept exercise placeholder',
        "deep_dive": """The first next() call executes until the first yield, returning 1 and suspending state. The second next() call resumes, increments count to 2, and yields 2. The print function receives and outputs this 2.""",
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
                "hint": "Return True to pass the concept check.",
                "data": """\
def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count += 1

counter = count_up_to(3)
next(counter)
print(next(counter))""",
                "evaluation_criteria": ["Understanding of concept"],
                "solution_code": """\
result = True""",
                "expected_output": True,
                "big_o_explanation": "Constant time implementation.",
                "follow_up_probes": ["Can you explain the limitations?"]
            }
        ]
    }
