import pandas as pd

def get_exercise():
    return {
        "title": "String Rotation",
        "description": "Assume you have a method `isSubstring` which checks if one word is a substring of another. Given two strings, `s1` and `s2`, write code to check if `s2` is a rotation of `s1` using only one call to `isSubstring` (e.g., 'waterbottle' is a rotation of 'erbottlewat').",
        "data": pd.DataFrame({
            "s1": ["waterbottle", "hello", "apple", "abc"],
            "s2": ["erbottlewat", "llohe", "pleap", "cab"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "If `s2` is a rotation of `s1`, then `s2` will always be a substring of `s1 + s1`. First, check that they are the same length and not empty.",
        "hint_sql": "Not applicable",
        "solution_python": """
def is_rotation(s1, s2):
    # Must be same length and not empty
    if len(s1) == len(s2) and len(s1) > 0:
        # Concatenate s1 with itself
        s1s1 = s1 + s1
        # Check if s2 is a substring of s1s1
        return s2 in s1s1
    return False

df["is_rotation"] = df.apply(lambda row: is_rotation(row["s1"], row["s2"]), axis=1)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "This elegant trick reduces the problem from potentially O(N^2) manual rotation checks to a single substring search on a concatenated string. In Python, the `in` operator uses efficient substring search algorithms (like Boyer-Moore or variations), typically running in O(N+M) time, where N is `len(s1s1)` and M is `len(s2)`. Therefore, the time complexity is O(N). The space complexity is also O(N) to store the concatenated string.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "The Core Substring Trick",
                "scenario": "You are given two non-empty strings `s1` and `s2` that are guaranteed to be the exact same length. Write a function to check if `s2` is a rotation of `s1`. You may only use an efficient substring check (e.g., `in`), rather than manually rotating the string character by character.",
                "hint": "If `s2` is a rotation of `s1`, imagine writing `s1` twice in a row (i.e., `s1 + s1`). Where would `s2` appear inside it?",
                "data": pd.DataFrame({
                    "s1": ["waterbottle", "hello", "data engineer", "python"],
                    "s2": ["erbottlewat", "llohe", "neerdata engi", "nophty"]
                }),
                "evaluation_criteria": [
                    "Understanding of the optimal math/string property (`s2` in `s1 + s1`).",
                    "Ability to correctly apply a substring check.",
                    "Comfort with multi-word strings and maintaining spaces."
                ],
                "solution_code": """\
def is_rotation(s1, s2):
    # s1 + s1 trick to easily find rotations
    s1s1 = s1 + s1
    return s2 in s1s1

df["is_rotation"] = df.apply(lambda row: is_rotation(row["s1"], row["s2"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "s1": ["waterbottle", "hello", "data engineer", "python"],
                    "s2": ["erbottlewat", "llohe", "neerdata engi", "nophty"],
                    "is_rotation": [True, True, True, False]
                }),
                "follow_up_probes": [
                    "Time Complexity: What is the time complexity of the `in` operator in Python under the hood?",
                    "Space Complexity: Generating `s1 + s1` takes O(N) space. Is there a way to do this in purely O(1) space if we manually verify characters with modulo arithmetic?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Length Validation",
                "scenario": "Now, the function might receive strings of different lengths. For example, `s2` might just be a shorter substring of `s1 + s1` but not a full rotation. Ensure your logic only returns `True` for actual valid rotations.",
                "hint": "A valid rotation must have the exact same length as the original string.",
                "data": pd.DataFrame({
                    "s1": ["waterbottle", "hello", "data engineer", "python", "waterbottle", "apple"],
                    "s2": ["erbottlewat", "llohe", "neerdata engi", "nophty", "water", "pleapp"]
                }),
                "evaluation_criteria": [
                    "Recognizing false positives caused by the `s1 + s1` trick.",
                    "Adding boundary checks (length condition) seamlessly into existing logic."
                ],
                "solution_code": """\
def is_rotation(s1, s2):
    # A rotation must have the exact same length as the original
    if len(s1) != len(s2):
        return False
        
    s1s1 = s1 + s1
    return s2 in s1s1

df["is_rotation"] = df.apply(lambda row: is_rotation(row["s1"], row["s2"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "s1": ["waterbottle", "hello", "data engineer", "python", "waterbottle", "apple"],
                    "s2": ["erbottlewat", "llohe", "neerdata engi", "nophty", "water", "pleapp"],
                    "is_rotation": [True, True, True, False, False, False]
                }),
                "follow_up_probes": [
                    "Order of Evaluation: Does it matter if you check the length before or after the concatenation and substring check?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Empty Strings & Edge Cases",
                "scenario": "Handling absolute edge cases perfectly is critical for production code. Update your function to handle empty strings gracefully. For the context of this exercise, an empty string should not be considered a valid rotation (`is_rotation` should return `False` if both strings are empty).",
                "hint": "Ensure both strings have a length strictly greater than 0 before checking rotations.",
                "data": pd.DataFrame({
                    "s1": ["waterbottle", "hello", "data engineer", "python", "waterbottle", "apple", "", "a", " ", ""],
                    "s2": ["erbottlewat", "llohe", "neerdata engi", "nophty", "water", "pleapp", "", "a", " ", "a"]
                }),
                "evaluation_criteria": [
                    "Handling edge cases flawlessly (empty strings, single characters, purely empty space strings).",
                    "Preventing illogical positive returns for zero-length strings."
                ],
                "solution_code": """\
def is_rotation(s1, s2):
    # Must be same length and strictly greater than 0
    if len(s1) == len(s2) and len(s1) > 0:
        s1s1 = s1 + s1
        return s2 in s1s1
    return False

df["is_rotation"] = df.apply(lambda row: is_rotation(row["s1"], row["s2"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "s1": ["waterbottle", "hello", "data engineer", "python", "waterbottle", "apple", "", "a", " ", ""],
                    "s2": ["erbottlewat", "llohe", "neerdata engi", "nophty", "water", "pleapp", "", "a", " ", "a"],
                    "is_rotation": [True, True, True, False, False, False, False, True, True, False]
                }),
                "follow_up_probes": [
                    "Validation Constraints: Why might an interviewer define an empty string not being a rotation of an empty string?",
                    "Reviewing Code: Is this solution complete? Is there any input you could pass that would cause a runtime error?"
                ]
            }
        ]
    }
