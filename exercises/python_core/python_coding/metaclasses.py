import pandas as pd

def get_exercise():
    return {
        "title": "Metaclasses and the Singleton Pattern",
        "subtitle": "metaclasses",
        "description": "Consider the following code utilizing a metaclass:\n\n```python\nclass SingletonMeta(type):\n    _instances = {}\n    def __call__(cls, *args, **kwargs):\n        if cls not in cls._instances:\n            cls._instances[cls] = super().__call__(*args, **kwargs)\n        return cls._instances[cls]\n\nclass Database(metaclass=SingletonMeta):\n    pass\n\ndb1 = Database()\ndb2 = Database()\n```\n\nWhat is the underlying mechanism that ensures `db1 is db2` evaluates to True?",
        "difficulty_level": "hard",
        "source_inspiration": "Anki Deck",
        "data": pd.DataFrame({"class_name": ["Database", "Database"], "instance_id": ["0x1A2B", "0x1A2B"]}),
        "allowed_modes": ["Python"],
        "hint_python": "When you call `Database()`, which method of the metaclass gets invoked? Does `__new__` execute first, or does the metaclass intercept it?",
        "solution_python": 'result = "The metaclass overrides __call__, intercepting the instantiation process of the Database class so it only allocates memory and initializes an instance if one does not already exist."',
        "deep_dive": """**Why this is correct (Lead Engineer Perspective):**

To understand metaclasses, you must remember that **classes are just objects too**. In Python, the default metaclass for all classes is `type`. When you define `class Database:`, Python uses `type` to create the `Database` class object.

By specifying `metaclass=SingletonMeta`, we tell Python to use our custom metaclass instead of `type`. 

When you instantiate an object by running `Database()`, you are actually executing the `__call__` method of its metaclass (`SingletonMeta`). 
This is the critical interception point. Inside `SingletonMeta.__call__`:
1. We check if `cls` (the `Database` class) is already a key in the `_instances` dictionary.
2. If it is NOT, we call `super().__call__(*args, **kwargs)`. This delegates back to `type.__call__`, which formally triggers `Database.__new__` (to allocate memory) and `Database.__init__` (to initialize the instance). We save this new instance.
3. If it IS in the dictionary, we skip creation entirely and return the cached instance.

Therefore, `db1` and `db2` both point to the exact same memory address.

- Option A is incorrect because `__init__` does not clear memory; it initializes variables after memory is allocated.
- Option C is incorrect as Python has no built-in automatic class caching mechanism for this.
- Option D is incorrect because the interception happens *before* `Database.__new__` is even invoked. It happens at the metaclass level via `__call__`.""",
        "big_o_explanation": "O(1) - Checking the `_instances` dictionary operates in constant time.",
        
        "mcq_questions": [
             {
                 "question": "What is the underlying mechanism that ensures `db1 is db2` evaluates to True in the provided Singleton metaclass code?",
                 "stage_number": 1,
                 "options": [
                     {"label": "A", "text": "The metaclass overrides __init__ to clear previously allocated memory blocks.", "is_correct": False},
                     {"label": "B", "text": "The metaclass overrides __call__, intercepting the instantiation process of the Database class so it only allocates memory and initializes an instance if one does not already exist.", "is_correct": True},
                     {"label": "C", "text": "Python's memory manager automatically caches classes without defined variables.", "is_correct": False},
                     {"label": "D", "text": "The __new__ method of the Database class intercepts the creation.", "is_correct": False},
                 ],
                 "explanation": "When you invoke Database(), you are actually invoking the __call__ method of its metaclass (SingletonMeta). By overriding __call__, the metaclass checks the internal _instances dictionary before allowing super().__call__ (which triggers __new__ and __init__ of the actual class) to execute, effectively intercepting instantiation to enforce the Singleton pattern."
             }
        ],

        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Metaclasses and the Singleton Pattern",
                "scenario": "Consider the following code utilizing a metaclass:\n\n```python\nclass SingletonMeta(type):\n    _instances = {}\n    def __call__(cls, *args, **kwargs):\n        if cls not in cls._instances:\n            cls._instances[cls] = super().__call__(*args, **kwargs)\n        return cls._instances[cls]\n\nclass Database(metaclass=SingletonMeta):\n    pass\n\ndb1 = Database()\ndb2 = Database()\n```\n\nWhat is the underlying mechanism that ensures `db1 is db2` evaluates to True?",
                "hint": "When you call `Database()`, which method of the metaclass gets invoked? Does `__new__` execute first, or does the metaclass intercept it?",
                "data": pd.DataFrame({"class_name": ["Database", "Database"], "instance_id": ["0x1A2B", "0x1A2B"]}),
                "evaluation_criteria": ["Understanding of Python's object model and metaclasses", "Differentiating between class instantiation methods like __call__, __new__, and __init__"],
                "solution_code": 'result = "The metaclass overrides __call__, intercepting the instantiation process of the Database class so it only allocates memory and initializes an instance if one does not already exist."',
                "expected_output": 'The metaclass overrides __call__, intercepting the instantiation process of the Database class so it only allocates memory and initializes an instance if one does not already exist.',
                "big_o_explanation": "O(1) - Checking the `_instances` dictionary operates in constant time.",
                "follow_up_probes": ["How does this approach compare to overriding `__new__` on the class itself?", "Is this metaclass thread-safe? How would you make it thread-safe?"]
            }
        ]
    }
