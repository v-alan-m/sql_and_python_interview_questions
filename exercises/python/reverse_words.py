import pandas as pd

def get_exercise():
    return {
        "title": "Reverse Words",
        "description": "Given a column of sentences, reverse the order of the words in each sentence while keeping the words themselves intact. Multiple spaces should be reduced to a single space.",
        "data": pd.DataFrame({
            "sentence": [
                "Hello world", 
                "  Python   is awesome  ", 
                "Data Engineering prep"
            ]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Use the `.split()` method (with no arguments, it handles multiple spaces automatically) to break the sentence into a list of words. Reverse that list, and then join it back together with spaces.",
        "hint_sql": "Not applicable",
        "solution_python": """
def reverse_sentence(sentence):
    # split() without arguments handles multiple whitespaces automatically
    words = str(sentence).split()
    # Reverse the list of words and join with a single space
    return " ".join(words[::-1])

df["reversed"] = df["sentence"].apply(reverse_sentence)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "String splitting and joining in Python happens in O(N) time complexity, where N is the length of the string. The list reversal `words[::-1]` also operates in O(K) where K is the number of words. The space complexity is O(N) to store the intermediate list of words and the new string."
    }
