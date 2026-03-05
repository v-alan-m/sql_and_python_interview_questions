import pandas as pd

def get_exercise():
    return {
        "title": "Last Word Length",
        "description": "Given a column of strings consisting of words and spaces, return the length of the last word in the string. A word is a maximal substring consisting of non-space characters only. Handle potential trailing spaces gracefully.",
        "data": pd.DataFrame({
            "text": [
                "Hello World", 
                "   fly me   to   the moon  ", 
                "luffy is still joyboy"
            ]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Use `.strip()` to remove leading/trailing spaces, then `.split()` by spaces. The last word is at index `[-1]`. Calculate the `.copy()` length of that element.",
        "hint_sql": "",
        "solution_python": '''\ndef length_of_last_word(s):\n    # Strip arbitrary padding on edges\n    s = s.strip()\n    if not s:\n        return 0\n        \n    # Split by spaces and grab the length of the last element\n    words = s.split()\n    return len(words[-1])\n\n# Alternative pointer approach (O(1) space): \n# def length_last_opt(s):\n#     length = 0\n#     for i in range(len(s) - 1, -1, -1):\n#         if s[i] != ' ':\n#             length += 1\n#         elif length > 0:\n#             break\n#     return length\n\ndf["last_word_length"] = df["text"].apply(length_of_last_word)\nresult = df\n''',
        "solution_sql": "",
        "deep_dive": "The `.split()` approach converts the entire string to a list of tokens, using O(N) space. However, we only care about the *last* word. An optimal backward iteration (the commented code) traverses from the tail backward, breaking early once the final word boundary is hit, executing in O(1) space and strictly O(K) time where K is the distance from the end of string to the end of the last word."
    }
