import pandas as pd

def get_exercise():
    return {
        "title": "Keyboard Row",
        "description": "Given an array of words, return the words that can be typed using letters of the alphabet on only one row of an American QWERTY keyboard (e.g., 'Alaska' is on the middle row, so it should be kept).",
        "data": pd.DataFrame({
            "word": ["Hello", "Alaska", "Dad", "Peace"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Define three `set`s of characters, one for each keyboard row. Convert each word into a `set` of its lowercase characters. Use the subset method (`<=` operator) to check if the word's characters are completely contained within any of the three row sets.",
        "hint_sql": "Not applicable",
        "solution_python": """
def check_single_row(word):
    # Define row sets (lowercase)
    row1 = set("qwertyuiop")
    row2 = set("asdfghjkl")
    row3 = set("zxcvbnm")
    
    # Convert word to a set of lowercase letters
    word_set = set(str(word).lower())
    
    # Check if the word set is a subset of any row
    # The <= operator checks for subset in Python sets
    return (word_set <= row1) or (word_set <= row2) or (word_set <= row3)

# Filter the dataframe keeping only rows that evaluate to True
df_filtered = df[df["word"].apply(check_single_row)].reset_index(drop=True)
result = df_filtered
""",
        "solution_sql": "Not applicable",
        "deep_dive": "Converting a word to a Set takes O(W) time where W is word length. Checking `subset <= row_set` also takes O(W) operations sequentially. Sets provide highly efficient subset and intersection calculations compared to iterating through arrays manually. Overall time complexity across N words of average length W is O(N * W)."
    }
