import pandas as pd

def get_exercise():
    return {
        "title": "Garbage Collection",
        "subtitle": "Core python concepts",
        "description": """In Python, standard memory management relies heavily on reference counting. However, which of the following scenarios specifically requires Python's generational cyclic garbage collector to intervene to prevent memory leaks?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": "No specific code setup required for this conceptual problem.",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = "Two custom object instances that maintain attributes pointing to each other, creating an isolated island after their original variables are deleted."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**
This question tests your knowledge of Python's dual-strategy memory management. As a lead engineer, diagnosing memory leaks in long-running services requires understanding how cyclic references occur and how they are resolved.

1. **Primary Strategy (Reference Counting):** Python primarily manages memory by keeping a count of how many references point to an object. When you delete a variable (`del x`), the count drops. If it hits zero, the memory is instantly freed.
2. **The Cyclic Flaw:** If `Object A` has an attribute pointing to `Object B`, and `Object B` has an attribute pointing to `Object A`, their internal reference counts are `1`. If you delete the global variables pointing to A and B, their counts remain at `1`. Standard reference counting will *never* free them because the count never reaches zero. They form an unreachable "island" in memory.
3. **The Fallback Strategy (Generational GC):** To solve this, Python utilizes a background Generational Garbage Collector. It periodically sweeps through objects in memory to detect these isolated cycles and safely tear them down.

While recursive calls cause a stack overflow and file connections leak file descriptors, only the cyclic reference specifically triggers the intervention of the generational cyclic GC.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """In Python, standard memory management relies heavily on reference counting. However, which of the following scenarios specifically requires Python's generational cyclic garbage collector to intervene to prevent memory leaks?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """A large list of immutable integers being repeatedly overwritten.""", "is_correct": False},
                     {"label": "B", "text": """Two custom object instances that maintain attributes pointing to each other, creating an isolated island after their original variables are deleted.""", "is_correct": True},
                     {"label": "C", "text": """Deeply nested recursive function calls that exceed the recursion depth limit.""", "is_correct": False},
                     {"label": "D", "text": """Opening a file connection without using a context manager or explicitly calling close().""", "is_correct": False},
                 ],
                 "explanation": """Reference counting immediately deallocates an object when its count hits zero. However, if object A references object B, and B references A, their internal reference counts remain at least 1 even if all external variables pointing to them are deleted. The cyclic garbage collector periodically sweeps for these unreachable \"islands\" of memory to reclaim them."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """In Python, standard memory management relies heavily on reference counting. However, which of the following scenarios specifically requires Python's generational cyclic garbage collector to intervene to prevent memory leaks?

""",
                "hint": "Standard reference counting fails when objects hold references to each other but are disconnected from the main program scope.",
                "data": "No specific code setup required for this conceptual problem.",
                "evaluation_criteria": ["Deep understanding of Python memory management", "Ability to diagnose memory leaks", "Knowledge of Reference Counting vs Generational GC"],
                "solution_code": 'result = "Two custom object instances that maintain attributes pointing to each other, creating an isolated island after their original variables are deleted."',
                "expected_output": "Two custom object instances that maintain attributes pointing to each other, creating an isolated island after their original variables are deleted.",
                "big_o_explanation": "O(1) concept. However, running the cyclic GC is computationally expensive and runs asynchronously.",
                "follow_up_probes": ["How can you manually trigger or disable the cyclic garbage collector?", "What is the weakref module and how does it prevent this issue?"]
            }
        ]
    }
