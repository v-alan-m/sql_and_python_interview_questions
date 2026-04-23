import pandas as pd

def get_exercise():
    return {
        "title": "Metaclasses",
        "subtitle": "Core python concepts",
        "description": """Consider the following code utilizing a metaclass:\n\nWhat is the underlying mechanism that ensures `db1 is db2` evaluates to True?\n\n""",
        "difficulty_level": "mid",
        "source_inspiration": "Anki Deck",
        "data": """\
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    pass

db1 = Database()
db2 = Database()""",
        "allowed_modes": ["Python"],
        "hint_python": "Review the concept detailed in the multiple choice section.",
        "solution_python": 'result = True # Concept exercise placeholder',
        "deep_dive": """When you invoke Database(), you are actually invoking the __call__ method of its metaclass (SingletonMeta). By overriding __call__, the metaclass checks the internal _instances dictionary before allowing super().__call__ (which triggers __new__ and __init__ of the actual class) to execute, effectively intercepting instantiation to enforce the Singleton pattern.""",
        "big_o_explanation": "O(1) - Concept exploration",

        "mcq_questions": [
             {
                 "question": """Consider the following code utilizing a metaclass:\n\nWhat is the underlying mechanism that ensures `db1 is db2` evaluates to True?\n\n""",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": """The metaclass overrides __init__ to clear previously allocated memory blocks.""", "is_correct": False},
                     {"label": "B", "text": """The metaclass overrides __call__, intercepting the instantiation process of the Database class so it only allocates memory and initializes an instance if one does not already exist.""", "is_correct": True},
                     {"label": "C", "text": """Python's memory manager automatically caches classes without defined variables.""", "is_correct": False},
                     {"label": "D", "text": """The __new__ method of the Database class intercepts the creation.""", "is_correct": False},
                 ],
                 "explanation": """When you invoke Database(), you are actually invoking the __call__ method of its metaclass (SingletonMeta). By overriding __call__, the metaclass checks the internal _instances dictionary before allowing super().__call__ (which triggers __new__ and __init__ of the actual class) to execute, effectively intercepting instantiation to enforce the Singleton pattern."""
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Concept Implementation",
                "scenario": """Consider the following code utilizing a metaclass:

What is the underlying mechanism that ensures `db1 is db2` evaluates to True?

""",
                "hint": "Examine the __call__ method in the metaclass. When does a metaclass's __call__ fire relative to a standard class's __init__?",
                "data": """\
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    pass

db1 = Database()
db2 = Database()""",
                "evaluation_criteria": ["Advanced OOP comprehension", "Understanding of the class instantiation lifecycle", "Familiarity with the Singleton pattern"],
                "solution_code": """\
result = \"\"\"Correct Answer: The metaclass overrides __call__, intercepting the instantiation process of the Database class so it only allocates memory and initializes an instance if one does not already exist.

**Why this is correct (Lead Engineer Perspective):**
This question evaluates your understanding of Python's class creation mechanics and the Singleton design pattern. As a lead engineer, you must understand how instantiation works at the interpreter level to design robust system architectures.

Here is the step-by-step architectural breakdown:
1. **The Role of __call__:** In Python, putting parentheses after an object (like `Database()`) invokes its `__call__` method. Since `Database` is an instance of `SingletonMeta`, `Database()` triggers `SingletonMeta.__call__`.
2. **Interception:** Before Python's default memory allocator (`__new__`) or initializer (`__init__`) runs for the `Database` class, the metaclass steps in.
3. **The State Dictionary:** The metaclass checks its own `_instances` dictionary. If `Database` is not in there, it calls `super().__call__` to actually allocate memory and initialize the object, storing the result in the dictionary.
4. **Returning the Singleton:** When `db2 = Database()` is executed, the metaclass sees that the instance already exists in the dictionary and simply returns the cached reference. Thus, `db1 is db2` evaluates to True.

Understanding metaclasses allows leads to write highly abstracted framework-level code (like Django models or ORMs) that handle boilerplate logic automatically.\"\"\"""",
                "expected_output": """Correct Answer: The metaclass overrides __call__, intercepting the instantiation process of the Database class so it only allocates memory and initializes an instance if one does not already exist.

**Why this is correct (Lead Engineer Perspective):**
This question evaluates your understanding of Python's class creation mechanics and the Singleton design pattern. As a lead engineer, you must understand how instantiation works at the interpreter level to design robust system architectures.

Here is the step-by-step architectural breakdown:
1. **The Role of __call__:** In Python, putting parentheses after an object (like `Database()`) invokes its `__call__` method. Since `Database` is an instance of `SingletonMeta`, `Database()` triggers `SingletonMeta.__call__`.
2. **Interception:** Before Python's default memory allocator (`__new__`) or initializer (`__init__`) runs for the `Database` class, the metaclass steps in.
3. **The State Dictionary:** The metaclass checks its own `_instances` dictionary. If `Database` is not in there, it calls `super().__call__` to actually allocate memory and initialize the object, storing the result in the dictionary.
4. **Returning the Singleton:** When `db2 = Database()` is executed, the metaclass sees that the instance already exists in the dictionary and simply returns the cached reference. Thus, `db1 is db2` evaluates to True.

Understanding metaclasses allows leads to write highly abstracted framework-level code (like Django models or ORMs) that handle boilerplate logic automatically.""",
                "big_o_explanation": "O(1) Time and Space for subsequent instantiations, due to dictionary lookups.",
                "follow_up_probes": ["Is this Singleton implementation thread-safe? How would you make it so?", "Why use a metaclass here instead of a simple class decorator?"]
            }
        ]
    }
