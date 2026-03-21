import pandas as pd

def get_exercise():
    return {
        "title": "Anagram Checker",
        "subtitle": "Loops",
        "description": "Check if two strings are anagrams of each other. Return True if they are, False otherwise. Ignore spaces and case.",
        "data": pd.DataFrame({
            "word1": ["listen", "triangle", "hello", "Dormitory"],
            "word2": ["silent", "integral", "world", "dirty room"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Remove spaces and make both strings lowercase. Then, you can either compare their sorted versions or use the `collections.Counter` class to count character frequencies.",
        "hint_sql": "Not applicable",
        "solution_python": """\
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
        "big_o_explanation": "For an anagram check, the time complexity `Counter(w1) == Counter(w2)` is **O(N)** where N is the length of the string, as it simply iterates through the characters to build a frequency map. Space complexity is **O(C)** where C is the number of distinct characters (up to 26 for English letters). This is significantly more optimal than sorting both strings first, which would take **O(N log N)** time.",
        "deep_dive": "Using `Counter` to tally frequencies runs in O(N) time complexity, where N is the length of the string. Sorting both strings would take O(N log N) time, making the frequency counting approach slightly more optimal for larger strings. Space complexity for counting is O(C) where C is the number of distinct characters (e.g., 26 for English letters).",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Lowercase Words",
                "scenario": "Let's start with a warm-up. Can you write a function to check if two single, lowercase words are anagrams of each other? Return True if they are, False otherwise.",
                "hint": "You can compare the sorted versions of the strings, or count the frequencies of each character using `collections.Counter` to see if they match exactly.",
                "data": pd.DataFrame({
                    "word1": ["listen", "triangle", "hello", "rat"],
                    "word2": ["silent", "integral", "world", "car"]
                }),
                "evaluation_criteria": [
                    "Basic understanding of what an anagram is.",
                    "Capability to execute frequency counting or character sorting.",
                    "Applying a function across two dataframe columns."
                ],
                "solution_code": """\
from collections import Counter

def is_anagram(w1, w2):
    return Counter(w1) == Counter(w2)

df["is_anagram"] = df.apply(lambda row: is_anagram(row["word1"], row["word2"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "word1": ["listen", "triangle", "hello", "rat"],
                    "word2": ["silent", "integral", "world", "car"],
                    "is_anagram": [True, True, False, False]
                }),
                "follow_up_probes": [
                    "What is the time complexity of your solution? (Sorting is O(N log N), while counting is O(N)).",
                    "Is there a difference in space complexity between sorting inplace vs keeping a frequency map?"
                ],
                "big_o_explanation": "Evaluating two lowercase words for anagram status using a frequency counter gives us a pristine **O(N) Time Complexity** (where N is the length of the string). We iterate over each character exactly once to populate the hash map. **Space Complexity is O(1)** (technically O(C) where C is the alphabet size), since the hash map size is bounded by the alphabet, not the length of the string. Sorting the strings instead would have incurred an **O(N log N)** time penalty."
            },
            {
                "stage_number": 2,
                "title": "Mixed Case Words",
                "scenario": "Great, that works. In reality, data entries usually have inconsistent casing. Can you update your logic to ignore case, so that 'Listen' and 'Silent' are correctly identified as anagrams?",
                "hint": "You will need to normalise both strings down to a common case, like lowercase, before you compare them.",
                "data": pd.DataFrame({
                    "word1": ["listen", "Listen", "Triangle", "hello", "Rat"],
                    "word2": ["silent", "Silent", "integral", "World", "cAr"]
                }),
                "evaluation_criteria": [
                    "String manipulation and text normalisation.",
                    "Safely handling method chains on string objects.",
                    "Handles both already-lowercase and mixed-case inputs."
                ],
                "solution_code": """\
from collections import Counter

def is_anagram(w1, w2):
    w1_clean = str(w1).lower()
    w2_clean = str(w2).lower()
    return Counter(w1_clean) == Counter(w2_clean)

df["is_anagram"] = df.apply(lambda row: is_anagram(row["word1"], row["word2"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "word1": ["listen", "Listen", "Triangle", "hello", "Rat"],
                    "word2": ["silent", "Silent", "integral", "World", "cAr"],
                    "is_anagram": [True, True, True, False, False]
                }),
                "follow_up_probes": [
                    "What happens if w1 or w2 are NaN or None in Pandas? How does str() behave?"
                ],
                "big_o_explanation": "Adding `.lower()` requires creating entirely new string objects in memory before the counting begins. Because strings are immutable in Python, this drops our **Space Complexity from O(1) to O(N)** since we have to allocate memory proportional to the input sizes. However, our **Time Complexity remains O(N)** because making a string lowercase is just another linear pass over the characters."
            },
            {
                "stage_number": 3,
                "title": "Multi-word Phrases with Spaces",
                "scenario": "Perfect. Now for the final curveball. Sometimes anagrams are entire phrases rather than single words, such as 'Dormitory' turning into 'dirty room'. We want to completely ignore whitespace when determining if two phrases are anagrams. Update your function to handle this.",
                "hint": "You need to strip out or replace the spaces completely before performing the lowercase conversion and counting. String `.replace()` might be helpful.",
                "data": pd.DataFrame({
                    "word1": ["listen", "Listen", "Dormitory", "hello", "The Morse Code"],
                    "word2": ["silent", "Silent", "dirty room", "world", "Here come dots"]
                }),
                "evaluation_criteria": [
                    "Handling substrings and non-alphabetic character removal.",
                    "Bringing it all together into a robust text comparison function.",
                    "Still handles plain lowercase and mixed-case single words correctly."
                ],
                "solution_code": """\
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
                "expected_output": pd.DataFrame({
                    "word1": ["listen", "Listen", "Dormitory", "hello", "The Morse Code"],
                    "word2": ["silent", "Silent", "dirty room", "world", "Here come dots"],
                    "is_anagram": [True, True, True, False, True]
                }),
                "follow_up_probes": [
                    "What if we had punctuation too? How would you replace all non-alphanumeric characters instead of just spaces?",
                    "Could we do a length check up front to fail-fast before doing counts and replacements?"
                ],
                "big_o_explanation": "Chaining `.replace()` introduces yet another linear O(N) pass across the string that generates a new object in memory. While we are doing more work (Replace -> Lower -> Counter), constants are dropped in Big O notation, meaning it is still `O(3N)` -> **O(N) Time Complexity**. A clever optimization would be to do a length check first `if len(w1) != len(w2): return False` to prevent O(N) computations on strings that obviously cannot be anagrams (though this requires them to be pre-cleaned)."
            }
        ]
    }
