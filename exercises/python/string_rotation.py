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
        "deep_dive": "This elegant trick reduces the problem from potentially O(N^2) manual rotation checks to a single substring search on a concatenated string. In Python, the `in` operator uses efficient substring search algorithms (like Boyer-Moore or variations), typically running in O(N+M) time, where N is `len(s1s1)` and M is `len(s2)`. Therefore, the time complexity is O(N). The space complexity is also O(N) to store the concatenated string."
    }
