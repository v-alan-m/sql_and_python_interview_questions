import pandas as pd

def get_exercise():
    return {
        "title": "Permutations",
        "description": "Given a string, print or return a list of all its valid permutations. You can assume all characters in the string are unique.",
        "data": pd.DataFrame({
            "string": ["abc", "ab", "a"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "You can use recursion. The base case is when the string is length 1. Otherwise, for each character in the string, extract it and recursively find permutations of the remaining characters, then prepend the extracted character. Alternatively, use `itertools.permutations`.",
        "hint_sql": "Not applicable",
        "solution_python": """
import itertools

def get_permutations(s):
    # Using itertools logic (Optimal for Python)
    # permutations returns tuples of characters, so we join them
    perms = itertools.permutations(s)
    return ["".join(p) for p in perms]

    # Recursive approach (good to know for interviews):
    # if len(s) <= 1:
    #     return [s]
    # result = []
    # for i, char in enumerate(s):
    #     remaining = s[:i] + s[i+1:]
    #     for p in get_permutations(remaining):
    #         result.append(char + p)
    # return result

df["permutations"] = df["string"].apply(get_permutations)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "Generating permutations is computationally heavy. For a string of length N, there are N! (N factorial) permutations. Therefore, both the time and space complexity are O(N * N!), as we must generate N! combinations and each combination takes O(N) space. `itertools.permutations` is implemented in C and is significantly faster than purely manual recursive approaches in Python."
    }
