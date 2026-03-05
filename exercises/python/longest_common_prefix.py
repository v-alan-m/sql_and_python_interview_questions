import pandas as pd

def get_exercise():
    return {
        "title": "Longest Common Prefix",
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
        "deep_dive": "Lexicographical sorting takes O(N log N) where N is the number of strings. Comparing only the first and last strings takes O(M) time, where M is the minimum length of the two strings. This sorting trick avoids the need for a nested loop structure doing vertical character-by-character scanning across all words, providing an elegant and terse Pythonic solution."
    }
