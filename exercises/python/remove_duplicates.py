import pandas as pd

def get_exercise():
    return {
        "title": "Remove Duplicates",
        "description": "Given a text column, remove all consecutive duplicate characters from the string. For example, 'aabbcc' becomes 'abc', and 'mississippi' becomes 'misisipi'.",
        "data": pd.DataFrame({
            "text": [
                "aabbcc", 
                "mississippi", 
                "hello world",
                "a"
            ]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Iterate through the string and append characters to a new list only if the character is different from the last character added to that list.",
        "hint_sql": "",
        "solution_python": '''\ndef remove_consecutive_duplicates(text):\n    if not text:\n        return text\n        \n    result = [text[0]]\n    \n    for i in range(1, len(text)):\n        # Only append if it's different from the most recently added char\n        if text[i] != result[-1]:\n            result.append(text[i])\n            \n    return "".join(result)\n\ndf["deduped_text"] = df["text"].apply(remove_consecutive_duplicates)\nresult = df\n''',
        "solution_sql": "",
        "deep_dive": "This is a simple state-tracking algorithm. By using the end of the `result` list `result[-1]` as our state tracker, we avoid needing a separate variable to keep track of the 'previous' character. The time complexity is exactly O(N) because we iterate through the sequence precisely once, and list appends in Python are amortized O(1)."
    }
