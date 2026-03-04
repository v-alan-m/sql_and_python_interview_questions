import pandas as pd

def get_exercise():
    return {
        "title": "Anagram Checker",
        "description": "Check if two strings are anagrams of each other. Return True if they are, False otherwise. Ignore spaces and case.",
        "data": pd.DataFrame({
            "word1": ["listen", "triangle", "hello", "Dormitory"],
            "word2": ["silent", "integral", "world", "dirty room"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Remove spaces and make both strings lowercase. Then, you can either compare their sorted versions or use the `collections.Counter` class to count character frequencies.",
        "hint_sql": "Not applicable",
        "solution_python": """
from collections import Counter

def is_anagram(w1, w2):
    # Clean strings: remove spaces and convert to lowercase
    w1_clean = str(w1).replace(" ", "").lower()
    w2_clean = str(w2).replace(" ", "").lower()
    
    # Compare character counts
    return Counter(w1_clean) == Counter(w2_clean)

df["is_anagram"] = df.apply(lambda row: is_anagram(row["word1"], row["word2"]), axis=1)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "Using `Counter` to tally frequencies runs in O(N) time complexity, where N is the length of the string. Sorting both strings would take O(N log N) time, making the frequency counting approach slightly more optimal for larger strings. Space complexity for counting is O(C) where C is the number of distinct characters (e.g., 26 for English letters)."
    }
