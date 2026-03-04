import pandas as pd

def get_exercise():
    return {
        "title": "Title Case Manual",
        "description": "Convert a string to title case manually (capitalize the first letter of each word and lowercase the rest) WITHOUT using Python's built-in `.title()` method. Handle multiple spaces by preserving them.",
        "data": pd.DataFrame({
            "string": ["hello world", "PYTHON is AWESOME", "  spaces   everywhere  "]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "You can process the string character by character. Maintain a boolean flag variable indicating whether the current character is the start of a new word, toggling it when space characters are encountered.",
        "hint_sql": "Not applicable",
        "solution_python": """
def manual_title_case(s):
    result = []
    # Start of string counts as start of word
    new_word = True
    
    for char in s:
        if char.isspace():
            result.append(char)
            # Next character starts a new word
            new_word = True
        elif new_word:
            result.append(char.upper())
            # Inside word now
            new_word = False
        else:
            result.append(char.lower())
            
    return "".join(result)

df["title_cased"] = df["string"].apply(manual_title_case)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "Python's built-in `.title()` performs poorly on words starting with numbers or apostrophes (e.g., 'they\\'re' -> 'They\\'Re'). A manual implementation gives precise control over tokenization boundaries. The loop runs exactly N times yielding an O(N) time complexity. Using list appending instead of string concatenation ensures O(N) performance rather than decaying into O(N^2)."
    }
