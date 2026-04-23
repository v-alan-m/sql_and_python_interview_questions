import pandas as pd

def get_exercise():
    return {
        "title": "Cyclic Garbage Collection",
        "subtitle": "garbage-collection",
        "description": "In Python, standard memory management relies heavily on reference counting. However, which of the following scenarios specifically requires Python's generational cyclic garbage collector to intervene to prevent memory leaks?",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": pd.DataFrame({"object_id": [1, 2], "ref_count": [1, 1], "is_cyclic": [True, True]}),
        "allowed_modes": ["Python"],
        "hint_python": "Consider what happens when reference counting fails. Reference counting goes to zero when an object has no references. What if two unreachable objects reference each other?",
        "solution_python": 'result = "Two custom object instances that maintain attributes pointing to each other, creating an isolated island after their original variables are deleted."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

Python's primary memory management system is reference counting. Every time you create a reference to an object, its reference count increments; when that reference goes out of scope or is reassigned, the count decrements. Once the count reaches zero, the memory is immediately deallocated.

However, reference counting has a fatal flaw: **reference cycles**.
If `object A` has an attribute pointing to `object B`, and `object B` has an attribute pointing to `object A`, their reference counts will both be at least `1`. Even if you delete all external variables referencing these objects, they form an "isolated island" of memory that reference counting alone can never reclaim, leading to a memory leak.

To solve this, CPython includes a supplemental **generational cyclic garbage collector** (`gc` module). The GC periodically pauses the application to scan for these unreachable isolated islands and reclaims the memory. 

- Option A is incorrect because overwriting variables simply decrements old reference counts and increments new ones; the old integers are properly cleaned up via standard reference counting.
- Option C is incorrect because a `RecursionError` exhausts the C call stack, which is unrelated to garbage collection.
- Option D is incorrect because unclosed files cause resource leaks (file descriptors), not necessarily memory leaks handled by the cyclic GC.""",
        "big_o_explanation": "O(N) - The cyclic garbage collector must traverse all tracked container objects (lists, dicts, instances) to detect and resolve cycles.",
        
        "mcq_questions": [
             {
                 "question": "In Python, standard memory management relies heavily on reference counting. However, which of the following scenarios specifically requires Python's generational cyclic garbage collector to intervene to prevent memory leaks?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "A large list of immutable integers being repeatedly overwritten.", "is_correct": False},
                     {"label": "B", "text": "Two custom object instances that maintain attributes pointing to each other, creating an isolated island after their original variables are deleted.", "is_correct": True},
                     {"label": "C", "text": "Deeply nested recursive function calls that exceed the recursion depth limit.", "is_correct": False},
                     {"label": "D", "text": "Opening a file connection without using a context manager or explicitly calling close().", "is_correct": False},
                 ],
                 "explanation": "Reference counting immediately deallocates an object when its count hits zero. However, if object A references object B, and B references A, their internal reference counts remain at least 1 even if all external variables pointing to them are deleted. The cyclic garbage collector periodically sweeps for these unreachable 'islands' of memory to reclaim them."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Cyclic Garbage Collection",
                "scenario": "In Python, standard memory management relies heavily on reference counting. However, which of the following scenarios specifically requires Python's generational cyclic garbage collector to intervene to prevent memory leaks?",
                "hint": "Consider what happens when reference counting fails. Reference counting goes to zero when an object has no references. What if two unreachable objects reference each other?",
                "data": pd.DataFrame({"object_id": [1, 2], "ref_count": [1, 1], "is_cyclic": [True, True]}),
                "evaluation_criteria": ["Understanding of Python's memory management", "Differentiating between reference counting and cyclic GC"],
                "solution_code": 'result = "Two custom object instances that maintain attributes pointing to each other, creating an isolated island after their original variables are deleted."',
                "expected_output": 'Two custom object instances that maintain attributes pointing to each other, creating an isolated island after their original variables are deleted.',
                "big_o_explanation": "O(N) - The cyclic garbage collector must traverse all tracked container objects (lists, dicts, instances) to detect and resolve cycles.",
                "follow_up_probes": ["How can you manually trigger or disable Python's garbage collector?", "Can you explain how generational garbage collection optimizes performance?"]
            }
        ]
    }
