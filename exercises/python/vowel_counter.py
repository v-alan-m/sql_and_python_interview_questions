import pandas as pd

def get_exercise():
    return {
        "title": "Vowel Counter",
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
        "deep_dive": "Checking membership `in` a Python `set` is an O(1) operation on average. Traversing the string takes O(N) time. The overall time complexity is therefore O(N). Space complexity is O(1) beyond the input itself, or O(N) depending on whether the `.lower()` function is executed on the entire string at once or if character-by-character conversion is leveraged."
    }
