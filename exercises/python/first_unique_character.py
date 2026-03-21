import pandas as pd

def get_exercise():
    return {
        "title": "First Unique Character",
        "subtitle": "Loops, Arrays / Lists, Hash Maps / Dictionaries",
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
        "deep_dive": "This approach uses two passes over the string. The first pass builds the hash map (Counter), taking O(N) time. The second pass checks the characters in order, taking at most O(N) time. Overall time complexity is linear O(N). Space complexity is O(1) because the English alphabet has a fixed limit of 26 characters, meaning the hash map size is bounded.",
        
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic First Unique",
                "scenario": "Find the first non-repeating character in a string. You can assume all inputs are lowercase and guaranteed to have at least one unique character.",
                "hint": "Count the frequency of each character, then find the first character with a count of 1.",
                "data": pd.DataFrame({"string": ["leetcode", "algorithm", "python code"]}),
                "evaluation_criteria": [
                    "Iterates over characters correctly",
                    "Uses appropriate data structure for frequency counting (like a dict or list)",
                    "Returns the correct character"
                ],
                "solution_code": """\\
from collections import Counter

def first_unique_stage_1(s):
    counts = Counter(s)
    for char in s:
        if counts[char] == 1:
            return char

df["first_unique"] = df["string"].apply(first_unique_stage_1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["leetcode", "algorithm", "python code"],
                    "first_unique": ["l", "a", "p"]
                }),
                "follow_up_probes": [
                    "What is the time and space complexity of your solution?",
                    "Could you do this without importing `Counter`?"
                ]
            },
            {
                "stage_number": 2,
                "title": "No Unique Character Edge Cases",
                "scenario": "Not all strings will have a unique character. Handle cases where every character repeats, or the string is empty. Return `None` in these situations.",
                "hint": "Ensure your loop safely finishes without returning if no character has a count of 1, and add a default return value.",
                "data": pd.DataFrame({"string": ["leetcode", "aabb", "zz", "", "algorithm", "no unique chars here either"]}),
                "evaluation_criteria": [
                    "Correctly returns None for completely repeating strings",
                    "Safely handles empty strings",
                    "Code remains clean without unnecessary nested if-statements"
                ],
                "solution_code": """\\
from collections import Counter

def first_unique_stage_2(s):
    counts = Counter(s)
    for char in s:
        if counts[char] == 1:
            return char
            
    return None

df["first_unique"] = df["string"].apply(first_unique_stage_2)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["leetcode", "aabb", "zz", "", "algorithm", "no unique chars here either"],
                    "first_unique": ["l", None, None, None, "a", "o"]
                }),
                "follow_up_probes": [
                    "How does `Counter` behave with an empty string?",
                    "Is the empty string check strictly necessary, or does the loop handle it naturally?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Case-Insensitive Counting",
                "scenario": "Strings can now contain mixtures of uppercase and lowercase letters. 'A' and 'a' should be treated as the SAME character when counting frequencies. However, you must return the character in its original case.",
                "hint": "Convert the string to lowercase when building your frequency map, but iterate over the original string to return the original case.",
                "data": pd.DataFrame({"string": ["LeetCode", "Aabb", "Swiss", "Racecar", "aabb"]}),
                "evaluation_criteria": [
                    "Normalises case when counting",
                    "Maintains original case when returning the output",
                    "Handles edge cases from Stage 2 properly"
                ],
                "solution_code": """\\
from collections import Counter

def first_unique_stage_3(s):
    # Count frequencies using a lowercase version
    counts = Counter(s.lower())
    
    # Iterate through original string, but look up lowercase char in counts
    for char in s:
        if counts[char.lower()] == 1:
            return char
            
    return None

df["first_unique"] = df["string"].apply(first_unique_stage_3)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["LeetCode", "Aabb", "Swiss", "Racecar", "aabb"],
                    "first_unique": ["L", None, "w", "e", None]
                }),
                "follow_up_probes": [
                    "Does `s.lower()` create a new string in memory? How does that affect space complexity?",
                    "Could you do this by keeping counts manually in a dictionary without an extra fully lowercased string copy?"
                ]
            },
            {
                "stage_number": 4,
                "title": "Filter Non-Alphabetic Characters",
                "scenario": "The input strings might contain spaces, numbers, or punctuation. We only care about finding the first unique *alphabetic* letter. Ignore all non-alphabetic characters entirely.",
                "hint": "Check if a character is a letter (e.g., using `.isalpha()`) both when counting and when searching for the first unique character.",
                "data": pd.DataFrame({"string": ["12345", "a 1 b 1 a", "S.w.i.s.s", "L33tCode!!", "aabb"]}),
                "evaluation_criteria": [
                    "Uses a conditional check like `.isalpha()` to filter characters",
                    "Only evaluates and counts alphabetic characters",
                    "Gracefully returns None if no alphabetic character is unique"
                ],
                "solution_code": """\\
from collections import Counter

def first_unique_stage_4(s):
    counts = Counter()
    
    # Count only alphabetic chars (case-insensitive)
    for char in s:
        if char.isalpha():
            counts[char.lower()] += 1
    
    for char in s:
        if char.isalpha() and counts[char.lower()] == 1:
            return char
            
    return None

df["first_unique"] = df["string"].apply(first_unique_stage_4)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["12345", "a 1 b 1 a", "S.w.i.s.s", "L33tCode!!", "aabb"],
                    "first_unique": [None, "b", "w", "L", None]
                }),
                "follow_up_probes": [
                    "Why is it better to populate our own dictionary manually here rather than building a new filtered string and calling `Counter` on it?",
                    "In a real data engineering pipeline, what library or tool might you use to clean a huge dataset of strings before processing?"
                ]
            }
        ]
    }
