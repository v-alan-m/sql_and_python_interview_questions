import pandas as pd

def get_exercise():
    return {
        "title": "Parameter Passing",
        "subtitle": "Parameter Passing",
        "description": """How are arguments passed to functions in Python?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": "No specific code setup required for this conceptual problem.",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = "By \"pass-by-assignment,\" where the function gets a copy of the reference to the object."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**
In Python, the terminology "pass-by-value" or "pass-by-reference" (common in languages like C++ or Java) doesn't strictly apply in the traditional sense. Instead, Python uses a mechanism best described as "pass-by-assignment" or "pass-by-object-reference." 

Here is the breakdown of why this happens:
* **Everything is an Object:** In Python, everything (including integers and strings) is an object. There are no "primitive types" that are treated differently from a memory management perspective.
* **Copy of the Reference:** When you pass an argument to a function, a local variable (the parameter) is created in the function's local namespace. This local variable points to the *exact same object* in memory as the original argument. It is essentially receiving a copy of the reference.
* **Mutable vs. Immutable Behavior:** 
    * If you pass a **mutable object** (like a `list` or `dict`) and modify it *in-place* (e.g., `my_list.append(1)`), the caller will see the change because both the local variable and the original variable point to the same modified object.
    * If you pass an **immutable object** (like an `int`, `string`, or `tuple`) and try to change it (e.g., `x += 1`), Python creates a completely *new* object and rebinds the local variable to this new object. The original variable outside the function continues to point to the original, unchanged object. 
* **Reassignment:** If you completely reassign the parameter inside the function, it simply breaks the local reference to the original object and binds the local name to a new object. It does *not* affect the caller's variable.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """How are arguments passed to functions in Python?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """Always by value; a copy of the argument is passed, and the original is never modified.""", "is_correct": False},
                     {"label": "B", "text": """Always by reference; a pointer to the original argument is passed and can always be changed.""", "is_correct": False},
                     {"label": "C", "text": """By \"pass-by-assignment,\" where the function gets a copy of the reference to the object.""", "is_correct": True},
                     {"label": "D", "text": """Primitive types are passed by value, while all objects are passed by reference.""", "is_correct": False},
                 ],
                 "explanation": """In Python, everything is an object. When passing arguments, the local variable receives a copy of the reference to the original object. Mutable objects modified in-place affect the caller, while reassignments or modifications to immutable objects create new objects locally."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """How are arguments passed to functions in Python?

""",
                "hint": "Focus on how Python treats object references under the hood, specifically the difference between mutable and immutable objects when passed to a local namespace.",
                "data": "No specific code setup required for this conceptual problem.",
                "evaluation_criteria": ["Understanding of pass-by-assignment", "Ability to distinguish mutable vs immutable behavior", "Clarity on namespace bindings"],
                "solution_code": 'result = "By \"pass-by-assignment,\" where the function gets a copy of the reference to the object."',
                "expected_output": "By \"pass-by-assignment,\" where the function gets a copy of the reference to the object.",
                "big_o_explanation": "O(1) Memory Overhead. Passing arguments only requires copying references, regardless of the underlying object size.",
                "follow_up_probes": ["How would this behavior affect a large pandas DataFrame passed into a function?", "How do you enforce immutability for a dictionary-like structure?"]
            }
        ]
    }
