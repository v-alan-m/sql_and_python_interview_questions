import pandas as pd

def get_exercise():
    return {
        "title": "First Unique Character",
        "description": "Given a string, find the first non-repeating character in it and return its character. If it doesn't exist, return an empty string or None. Assume the string contains only lowercase English letters.",
        "data": pd.DataFrame({
            "string": ["leetcode", "loveleetcode", "aabb", "z"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "You can use a dictionary or `collections.Counter` to count the frequency of each character in a first pass. In a second pass through the string, return the first character that has a count of 1.",
        "hint_sql": "Not applicable",
        "solution_python": """
from collections import Counter

def first_unique_char(s):
    # Count frequencies of each character
    counts = Counter(s)
    
    # Second pass: find the first one with a count of 1
    for char in s:
        if counts[char] == 1:
            return char
            
    return None

df["first_unique"] = df["string"].apply(first_unique_char)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "This approach uses two passes over the string. The first pass builds the hash map (Counter), taking O(N) time. The second pass checks the characters in order, taking at most O(N) time. Overall time complexity is linear O(N). Space complexity is O(1) because the English alphabet has a fixed limit of 26 characters, meaning the hash map size is bounded."
    }
