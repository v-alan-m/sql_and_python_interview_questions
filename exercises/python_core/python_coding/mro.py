import pandas as pd

def get_exercise():
    return {
        "title": "Multiple Inheritance and MRO",
        "subtitle": "mro",
        "description": "Consider the following Python code demonstrating multiple inheritance:\n\nWhat is the output printed to the console?",
        "difficulty_level": "hard",
        "source_inspiration": "Anki Deck",
        "data": """class A:
    def process(self): return "A"
class B(A):
    def process(self): return "B" + super().process()
class C(A):
    def process(self): return "C" + super().process()
class D(B, C):
    def process(self): return "D" + super().process()

obj = D()
print(obj.process())""",
        "hide_data": False,
        "allowed_modes": ["Python"],
        "hint_python": "Do not assume `super()` always calls the immediate parent class. `super()` traverses the Method Resolution Order (MRO) dynamically. Check `D.mro()`.",
        "solution_python": 'result = "DBCA"',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

Multiple inheritance in Python relies on an algorithm known as **C3 Linearization** to generate a consistent Method Resolution Order (MRO). The MRO is a flat, ordered list of classes that Python searches when a method is invoked.

For `class D(B, C)`, the C3 linearization algorithm guarantees two things:
1. Children precede their parents (D comes before B and C; B and C come before A).
2. The order of base classes is preserved (B comes before C because it was declared as `D(B, C)`).

This resolves the MRO of `D` to: `[D, B, C, A, object]`.

The biggest misconception among developers is that `super()` refers to the direct textual parent of the class it resides in. **This is false.** `super()` dynamically looks at the *instance's* MRO and delegates the call to the next class in that sequence.

Let's trace the execution of `obj.process()`:
1. `obj` is an instance of `D`. The call lands in `D.process()`, which returns `"D" + super().process()`. Here, `super()` finds `B` as the next class in the MRO.
2. We jump to `B.process()`, which returns `"B" + super().process()`. **Crucially**, `super()` here looks at the MRO `[D, B, C, A, object]`. The next class after `B` is **`C`**, not `A`.
3. We jump to `C.process()`, returning `"C" + super().process()`. The next class after `C` is `A`.
4. We jump to `A.process()`, which simply returns `"A"`.

Bubbling back up, we get `"D" + "B" + "C" + "A"`, resulting in `"DBCA"`. This specific arrangement prevents the "Diamond Problem" where `A`'s method might be called twice.

- Options A, C, and D are incorrect because they fail to properly evaluate the C3 Linearization order and the dynamic delegation behavior of `super()`.""",
        "big_o_explanation": "O(L) where L is the depth of the class hierarchy. MRO generation and attribute lookup occur linearly along the inheritance chain.",
        
        "mcq_questions": [
             {
                 "question": "What is the output printed to the console when executing the provided multiple inheritance code?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "DBCA", "is_correct": True},
                     {"label": "B", "text": "DBAC", "is_correct": False},
                     {"label": "C", "text": "DBA", "is_correct": False},
                     {"label": "D", "text": "DCBA", "is_correct": False},
                 ],
                 "explanation": "Python uses C3 linearization to determine the Method Resolution Order (MRO). For class D(B, C), the MRO is D -> B -> C -> A -> object. Crucially, super() delegates to the next class in the instance's overall MRO, not necessarily the immediate textual parent of the current class. Thus, B's super() delegates to C, resulting in the chain D -> B -> C -> A."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Multiple Inheritance and MRO",
                "scenario": "Consider the following Python code demonstrating multiple inheritance:\n\nWhat is the output printed to the console?",
                "hint": "Do not assume `super()` always calls the immediate parent class. `super()` traverses the Method Resolution Order (MRO) dynamically. Check `D.mro()`.",
                "data": """class A:
    def process(self): return "A"
class B(A):
    def process(self): return "B" + super().process()
class C(A):
    def process(self): return "C" + super().process()
class D(B, C):
    def process(self): return "D" + super().process()

obj = D()
print(obj.process())""",
                "hide_data": False,
                "evaluation_criteria": ["Understanding of C3 Linearization algorithm", "Dynamic delegation behavior of super() across multiple inheritance diamonds"],
                "solution_code": 'result = "DBCA"',
                "expected_output": 'DBCA',
                "big_o_explanation": "O(L) where L is the depth of the class hierarchy. MRO generation and attribute lookup occur linearly along the inheritance chain.",
                "follow_up_probes": ["What happens if you define `class D(C, B)` instead?", "Can a class hierarchy be rejected by Python? If so, why?"]
            }
        ]
    }
