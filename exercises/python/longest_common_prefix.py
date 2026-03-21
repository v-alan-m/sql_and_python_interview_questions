import pandas as pd

def get_exercise():
    return {
        "title": "Longest Common Prefix",
        "subtitle": "Loops, Arrays / Lists",
        "description": "Given a dataset where each row contains a list of words, find the longest common prefix string amongst the array of strings. If there is no common prefix, return an empty string.",
        "data": pd.DataFrame({
            "word_list": [
                ["flower", "flow", "flight"],
                ["dog", "racecar", "car"],
                ["interview", "internet", "internal"]
            ]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "You can sort the array of strings and just compare the first and the last string in the sorted array. Alternatively, iterating character by character through the first string and checking other strings works well.",
        "hint_sql": "",
        "solution_python": '''\ndef longest_common_prefix(strs):\n    if not strs:\n        return ""\n        \n    # Sorting alphabetically makes it so we only need to compare\n    # the first and last words to find the max common prefix.\n    strs.sort()\n    first = strs[0]\n    last = strs[-1]\n    \n    prefix = []\n    for i in range(min(len(first), len(last))):\n        if first[i] == last[i]:\n            prefix.append(first[i])\n        else:\n            break\n            \n    return "".join(prefix)\n\ndf["common_prefix"] = df["word_list"].apply(longest_common_prefix)\nresult = df\n''',
        "solution_sql": "",
        "deep_dive": "Lexicographical sorting takes O(N log N) where N is the number of strings. Comparing only the first and last strings takes O(M) time, where M is the minimum length of the two strings. This sorting trick avoids the need for a nested loop structure doing vertical character-by-character scanning across all words, providing an elegant and terse Pythonic solution.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Two Words Only",
                "scenario": "The input arrays will always contain exactly two strings. Write a simple character-by-character comparison to find their common prefix.",
                "hint": "Iterate over the indices from 0 to the minimum length of the two words, and check if the characters match. If they don't, you've found the end of the prefix.",
                "data": pd.DataFrame({
                    "word_list": [
                        ["flow", "flower"],
                        ["dog", "racecar"],
                        ["cat", "cat"]
                    ]
                }),
                "evaluation_criteria": [
                    "Basic array indexing and string slicing.",
                    "Correctly identifying the loop bounds (min length).",
                    "Early loop termination upon finding a mismatch."
                ],
                "solution_code": """\
def extract_prefix(strs):
    first, second = strs[0], strs[1]
    prefix = []
    for i in range(min(len(first), len(second))):
        if first[i] == second[i]:
            prefix.append(first[i])
        else:
            break
    return "".join(prefix)

df["common_prefix"] = df["word_list"].apply(extract_prefix)
result = df
""",
                "expected_output": pd.DataFrame({
                    "word_list": [
                        ["flow", "flower"],
                        ["dog", "racecar"],
                        ["cat", "cat"]
                    ],
                    "common_prefix": ["flow", "", "cat"]
                }),
                "follow_up_probes": [
                    "Time Complexity: What is the Big-O time complexity of your solution? (O(min(N, M)) where N and M are the lengths of the two words).",
                    "String Concatenation: Why use a list and `\"\".join()` instead of `+=` for building the string in Python?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Multiple Words",
                "scenario": "The arrays can now contain more than two strings, and they might include multi-word phrases. Find the longest common prefix across *all* strings in the array. Note that one of the test cases has multi-word elements.",
                "hint": "You could repeatedly apply your two-word prefix logic across the array. Alternatively, try sorting the array alphabetically first. If the array is sorted lexicographically, which words dictate the maximum possible prefix?",
                "data": pd.DataFrame({
                    "word_list": [
                        ["flower", "flow", "flight"],
                        ["dog", "racecar", "car"],
                        ["interview", "internet", "internal"],
                        ["data science", "data engineer", "data analyst"]
                    ]
                }),
                "evaluation_criteria": [
                    "Iterating across variable-length lists.",
                    "Ability to extend previous logic or invent a new optimal approach (e.g. lexicographical sorting).",
                    "Handling mixed data where some lists have common prefixes and others don't."
                ],
                "solution_code": """\
def longest_common_prefix(strs):
    # Sorting alphabetically makes it so we only need to compare
    # the first and last words to find the max common prefix.
    strs_sorted = sorted(strs)
    first = strs_sorted[0]
    last = strs_sorted[-1]
    
    prefix = []
    for i in range(min(len(first), len(last))):
        if first[i] == last[i]:
            prefix.append(first[i])
        else:
            break
            
    return "".join(prefix)

df["common_prefix"] = df["word_list"].apply(longest_common_prefix)
result = df
""",
                "expected_output": pd.DataFrame({
                    "word_list": [
                        ["flower", "flow", "flight"],
                        ["dog", "racecar", "car"],
                        ["interview", "internet", "internal"],
                        ["data science", "data engineer", "data analyst"]
                    ],
                    "common_prefix": ["fl", "", "inter", "data "]
                }),
                "follow_up_probes": [
                    "Algorithm Analysis: Compare the time complexity of the sorting approach vs the iterative sequential comparison. (Sorting is O(N*M log N) whereas sequential is O(N*M)). Which one is better?",
                    "Optimisation: Can this be done using a Divide and Conquer approach? Or a Trie?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Edge Cases & Robustness",
                "scenario": "The pipeline can provide messy arrays. The arrays might be completely empty, contain only a single word, or contain empty strings. Make your function robust to handle these edge cases without crashing.",
                "hint": "Add guard clauses before accessing indices. Think about how `min()` behaves with empty sequences, and how sorting handles empty strings.",
                "data": pd.DataFrame({
                    "word_list": [
                        ["flower", "flow", "flight"],
                        [],
                        ["singleword"],
                        ["", "empty"],
                        ["prefix", "prefix", "prefix", ""]
                    ]
                }),
                "evaluation_criteria": [
                    "Safe array access and guard clauses (checking if `strs` is empty).",
                    "Complete awareness of Python language edge cases (e.g. accessing `strs[0]` on `[]`)."
                ],
                "solution_code": """\
def longest_common_prefix_robust(strs):
    if not strs:
        return ""
        
    strs_sorted = sorted(strs)
    first = strs_sorted[0]
    last = strs_sorted[-1]
    
    prefix = []
    for i in range(min(len(first), len(last))):
        if first[i] == last[i]:
            prefix.append(first[i])
        else:
            break
            
    return "".join(prefix)

df["common_prefix"] = df["word_list"].apply(longest_common_prefix_robust)
result = df
""",
                "expected_output": pd.DataFrame({
                    "word_list": [
                        ["flower", "flow", "flight"],
                        [],
                        ["singleword"],
                        ["", "empty"],
                        ["prefix", "prefix", "prefix", ""]
                    ],
                    "common_prefix": ["fl", "", "singleword", "", ""]
                }),
                "follow_up_probes": [
                    "Empty Sequences: In python, how does `if not strs:` behave for empty lists vs arrays with empty strings?",
                    "Empty Strings during Sorting: Lexicographically, where do empty strings sort relative to populated strings? (They sort first)."
                ]
            }
        ]
    }
