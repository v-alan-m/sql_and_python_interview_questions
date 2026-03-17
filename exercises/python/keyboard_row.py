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
        "deep_dive": "Converting a word to a Set takes O(W) time where W is word length. Checking `subset <= row_set` also takes O(W) operations sequentially. Sets provide highly efficient subset and intersection calculations compared to iterating through arrays manually. Overall time complexity across N words of average length W is O(N * W).",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Top Row Only",
                "scenario": "The interviewer asks you to write a function that only returns words that can be typed entirely on the *top row* of a QWERTY keyboard ('qwertyuiop'). All inputs are guaranteed to be lowercase strings.",
                "hint": "Define a `set` containing the letters of the top row. Convert each word to a `set` and use the subset operator (`<=`) to check if the word's letters are completely contained within the top row set. Use boolean indexing to filter the DataFrame.",
                "data": pd.DataFrame({"word": ["type", "hello", "power", "world"]}),
                "evaluation_criteria": [
                    "Ability to define character sets.",
                    "Usage of set operations (`<=` or `.issubset()`).",
                    "Familiarity with Pandas `.apply()` for filtering."
                ],
                "solution_code": """\
def is_top_row(word):
    top_row = set("qwertyuiop")
    word_set = set(word)
    return word_set <= top_row

result = df[df["word"].apply(is_top_row)].reset_index(drop=True)""",
                "expected_output": pd.DataFrame({"word": ["type", "power"]}),
                "follow_up_probes": [
                    "What is the time complexity of converting a string to a set?",
                    "Are there any edge cases with an empty string here?"
                ]
            },
            {
                "stage_number": 2,
                "title": "All Three Rows (Lower Case)",
                "scenario": "Now extend your logic to support all letters. Return words that can be typed on *any single row* of the keyboard. Still lowercase words only.",
                "hint": "Define three separate sets, one for each row. Check if the word's character set is a subset of *any* of the three row sets using `or` conditions.",
                "data": pd.DataFrame({"word": ["tree", "dad", "peace", "cvs", "jazz"]}),
                "evaluation_criteria": [
                    "Extension of boolean logic to check multiple conditions (`or`).",
                    "Maintaining un-nested, clean logic."
                ],
                "solution_code": """\
def check_single_row(word):
    row1 = set("qwertyuiop")
    row2 = set("asdfghjkl")
    row3 = set("zxcvbnm")
    
    word_set = set(word)
    return (word_set <= row1) or (word_set <= row2) or (word_set <= row3)

result = df[df["word"].apply(check_single_row)].reset_index(drop=True)""",
                "expected_output": pd.DataFrame({"word": ["tree", "dad"]}),
                "follow_up_probes": [
                    "Is there a more dynamic way to check against the rows instead of hardcoding three `or` statements?",
                    "Would checking the rows in a specific order (e.g., top row first because it has the most vowels) improve the average performance?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Mixed Case and Robustness",
                "scenario": "The input data is getting messier. Inputs now include capital letters, and some rows might theoretically contain missing values (NaN) or numeric types (like integers). Ensure your function safely handles these to return only valid words while safely rejecting bad types.",
                "hint": "Converting `np.nan` or integers directly to strings implicitly produces `'nan'` or numbers. They naturally fail keyboard row set matching (since numbers aren't in the alphabet sets, and `'nan'` uses letters from multiple rows). Force string conversion before lowercase conversion: `str(word).lower()`.",
                "data": pd.DataFrame({
                    "word": ["Alaska", "Dad", "Peace", 404, None, "Type"]
                }),
                "evaluation_criteria": [
                    "Understanding of data type conversion pitfalls (`str(NaN) == 'nan'`).",
                    "Usage of `.lower()` before set conversion safely.",
                    "Robustness against Non-String types in Pandas."
                ],
                "solution_code": """\
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
result = df[df["word"].apply(check_single_row)].reset_index(drop=True)""",
                "expected_output": pd.DataFrame({"word": ["Alaska", "Dad", "Type"]}),
                "follow_up_probes": [
                    "How does `str(None)` behave, and why does your logic correctly discard it?",
                    "What's the overall time complexity of this filtered approach?",
                    "If we wanted to return a list of validity booleans instead of filtering the dataframe, how would you change it?"
                ]
            }
        ]
    }
