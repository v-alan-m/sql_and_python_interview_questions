import pandas as pd

def get_exercise():
    return {
        "title": "Vowel Counter",
        "subtitle": "Loops, Arrays / Lists, Sets",
        "description": "Count the number of vowels (a, e, i, o, u) in a given string. Ignore casing (e.g., both 'a' and 'A' count).",
        "data": pd.DataFrame({
            "string": ["Hello World", "Queueing problem", "Rhythm", "AI is cool"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Iterate through the string and check if the lowercase version of the character is `in` a set of vowels.",
        "hint_sql": "Not applicable",
        "solution_python": """
def count_vowels(s):
    vowels = set("aeiou")
    # Generator expression to count matching characters
    return sum(1 for char in str(s).lower() if char in vowels)

df["vowel_count"] = df["string"].apply(count_vowels)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "Checking membership `in` a Python `set` is an O(1) operation on average. Traversing the string takes O(N) time. The overall time complexity is therefore O(N). Space complexity is O(1) beyond the input itself, or O(N) depending on whether the `.lower()` function is executed on the entire string at once or if character-by-character conversion is leveraged.",
        "big_o_explanation": "### ⏱️ Optimal Big O Notation\n**Time Complexity:** `O(N)` where `N` is the length of the string. We iterate over the string once, and looking up a character inside a Python `set` has an average `O(1)` time complexity.\n**Space Complexity:** `O(1)` auxiliary space because the size of the set containing vowels is constant (`5` characters) and does not scale with the input string. (Note: explicitly calling `s.lower()` on the entire string first allocates a new `O(N)` string buffer).",

        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Lowercase Counting",
                "scenario": "You receive a DataFrame with a column 'string' containing simple, lowercase, single-word strings. Count the number of vowels (a, e, i, o, u) in each string and add a 'vowel_count' column.",
                "hint": "Write a helper function that iterates through each character and checks membership in a set of vowels. Apply it to the column with .apply().",
                "data": pd.DataFrame({
                    "string": ["hello", "python", "aeiou"]
                }),
                "evaluation_criteria": [
                    "Can the candidate write a basic character-iteration function?",
                    "Correct use of df.apply() to produce a new column.",
                    "Using a set for O(1) vowel membership checks."
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({"string": ["hello", "python", "aeiou"]})

def count_vowels(s):
    vowels = set("aeiou")
    return sum(1 for char in s if char in vowels)

df["vowel_count"] = df["string"].apply(count_vowels)
result = df""",
                "expected_output": pd.DataFrame({
                    "string": ["hello", "python", "aeiou"],
                    "vowel_count": [2, 1, 5]
                }),
                "follow_up_probes": [
                    "Why use a set instead of a string for the vowel lookup? → O(1) average-case membership test vs O(N) for a string/list.",
                    "What is the time complexity? → O(N × M) where N = rows, M = average string length.",
                    "Could you solve this without a loop using sum() and a generator expression? → Yes, which is exactly what this solution does."
                ],
                "big_o_explanation": "#### Stage 1: Basic Lowercase Counting\n**Time Complexity:** `O(N)` where `N` is the length of the string. Checking membership in a hash set is an `O(1)` operation. Across all rows, it becomes `O(R * N)` where `R` is the number of rows.\n**Space Complexity:** `O(1)` auxiliary space (excluding the output Pandas column) because the size of the vowel set is fixed at 5 characters."
            },
            {
                "stage_number": 2,
                "title": "Mixed Case & Multi-Word Strings",
                "scenario": "The data now includes uppercase letters and multi-word strings (e.g., 'Hello World'). Your count should be case-insensitive — both 'A' and 'a' count as vowels. Spaces are not vowels.",
                "hint": "Convert the string to lowercase with .lower() before iterating, so your vowel set only needs lowercase letters.",
                "data": pd.DataFrame({
                    "string": ["Hello World", "UPPERCASE TEST", "python", "AI is cool"]
                }),
                "evaluation_criteria": [
                    "Case-insensitive handling — does the candidate normalise with .lower()?",
                    "Multi-word strings — spaces are correctly ignored.",
                    "Mix of data from Stage 1 (simple lowercase) and new inputs (uppercase, multi-word)."
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({"string": ["Hello World", "UPPERCASE TEST", "python", "AI is cool"]})

def count_vowels(s):
    vowels = set("aeiou")
    return sum(1 for char in s.lower() if char in vowels)

df["vowel_count"] = df["string"].apply(count_vowels)
result = df""",
                "expected_output": pd.DataFrame({
                    "string": ["Hello World", "UPPERCASE TEST", "python", "AI is cool"],
                    "vowel_count": [3, 5, 1, 5]
                }),
                "follow_up_probes": [
                    "How much code changed from Stage 1? → Only one addition: .lower() on the input string. Everything else is identical.",
                    "What's the alternative to .lower() — could you use a larger vowel set instead? → Yes, set('aeiouAEIOU'), which avoids creating a new lowercase copy of the string.",
                    "Which approach is more memory-efficient for very long strings? → The larger vowel set avoids the .lower() copy, but the difference is negligible for typical inputs."
                ],
                "big_o_explanation": "#### Stage 2: Mixed Case & Multi-Word Strings\n**Time Complexity:** `O(N)`. We still check every character. The `s.lower()` method sweeps the string once taking `O(N)` time, and the generator expression sweeps it again taking `O(N)` time. `2N` simplifies to `O(N)`.\n**Space Complexity:** `O(N)` because `s.lower()` allocates and returns an entirely new lowercase string of length `N` in memory before the generator iteration begins. (Using `set('aeiouAEIOU')` instead without `.lower()` would keep it at `O(1)` space)."
            },
            {
                "stage_number": 3,
                "title": "Non-Alpha Characters & Numeric Strings",
                "scenario": "The input strings now contain digits, punctuation, and special characters (e.g., 'h3llo!', '12345'). Only alphabetic vowels should be counted — digits and symbols are never vowels.",
                "hint": "Your existing solution should already handle this if you're checking membership in a vowel set — digits and punctuation simply won't match. Verify, don't over-engineer.",
                "data": pd.DataFrame({
                    "string": ["h3llo w0rld!", "12345", "Hello World", "@e_m@il.com", "Queueing problem"]
                }),
                "evaluation_criteria": [
                    "Robustness against digits and special characters without adding explicit guards.",
                    "Recognising that the existing .lower() + vowel-set check naturally filters non-alpha characters.",
                    "Consecutive vowels in a single word (e.g., 'Queueing') — testing counting accuracy with dense vowel clusters."
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({"string": ["h3llo w0rld!", "12345", "Hello World", "@e_m@il.com", "Queueing problem"]})

def count_vowels(s):
    vowels = set("aeiou")
    return sum(1 for char in s.lower() if char in vowels)

df["vowel_count"] = df["string"].apply(count_vowels)
result = df""",
                "expected_output": pd.DataFrame({
                    "string": ["h3llo w0rld!", "12345", "Hello World", "@e_m@il.com", "Queueing problem"],
                    "vowel_count": [1, 0, 3, 3, 7]
                }),
                "follow_up_probes": [
                    "Did you need to change any code from Stage 2? → Ideally zero changes. A well-written vowel set check handles non-alpha characters automatically.",
                    "Walk through '@e_m@il.com' character by character. Which characters match? → 'e', 'i', and 'o' — the @, _, . are ignored by the set lookup.",
                    "What if the interviewer asked you to also count 'y' as a vowel in certain contexts? How would you modify the code? → Add 'y' to the vowel set, or implement conditional logic based on position."
                ],
                "big_o_explanation": "#### Stage 3: Non-Alpha Characters & Numeric Strings\n**Time Complexity:** `O(N)`. The presence of non-alpha characters does not alter how many characters we iterate through.\n**Space Complexity:** `O(N)` due to the `s.lower()` call, or `O(1)` if a case-insensitive set was used. Special characters do not affect the space scaling."
            },
            {
                "stage_number": 4,
                "title": "Empty Strings, No Vowels & Stress Cases",
                "scenario": "Final round. The data now includes edge cases: empty strings, strings with zero vowels, single-character strings, and a dense vowel string. Ensure your solution handles all of these without crashing.",
                "hint": "If your generator expression encounters an empty string, sum() returns 0 naturally — there's nothing to iterate. Verify that str(s).lower() guards against non-string inputs if needed.",
                "data": pd.DataFrame({
                    "string": ["", "rhythm", "b", "a", "Bcdfg Hjklm Npqrs", "aaaeeeiiiooo"]
                }),
                "evaluation_criteria": [
                    "Empty string handling — does the function return 0 without errors?",
                    "All-consonant strings — correct 0 count.",
                    "Single-character boundaries — a vowel vs a consonant.",
                    "Dense vowel string — accurate counting without off-by-one.",
                    "Code stability — ideally zero changes from Stage 3."
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({"string": ["", "rhythm", "b", "a", "Bcdfg Hjklm Npqrs", "aaaeeeiiiooo"]})

def count_vowels(s):
    vowels = set("aeiou")
    return sum(1 for char in str(s).lower() if char in vowels)

df["vowel_count"] = df["string"].apply(count_vowels)
result = df""",
                "expected_output": pd.DataFrame({
                    "string": ["", "rhythm", "b", "a", "Bcdfg Hjklm Npqrs", "aaaeeeiiiooo"],
                    "vowel_count": [0, 0, 0, 1, 0, 12]
                }),
                "follow_up_probes": [
                    "How much code changed from Stage 3? → Only the addition of str(s) to guard against potential non-string types. Core logic is unchanged.",
                    "What's the worst-case time complexity for a single string? → O(M) where M is the string length. Every character is checked exactly once.",
                    "At 10 million rows of data, how would you optimise beyond .apply()? → Vectorised approach: df['string'].str.lower().str.count(r'[aeiou]') avoids the Python-level loop entirely."
                ],
                "big_o_explanation": "#### Stage 4: Empty Strings, No Vowels & Stress Cases\n**Time Complexity:** `O(N)`.\n**Space Complexity:** `O(N)`. There are no major architectural shifts; handling stress cases properly with Python generators is inherently safe and stable on memory."
            }
        ]
    }
