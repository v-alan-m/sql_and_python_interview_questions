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
                "hint": "Return True to pass the concept check.",
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
                "evaluation_criteria": ["Understanding of concept"],
                "solution_code": """\
result = True""",
                "expected_output": True,
                "big_o_explanation": "Constant time implementation.",
                "follow_up_probes": ["Can you explain the limitations?"]
            }
        ]
    }
