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
        "deep_dive": "Python's built-in `.title()` performs poorly on words starting with numbers or apostrophes (e.g., 'they\\'re' -> 'They\\'Re'). A manual implementation gives precise control over tokenization boundaries. The loop runs exactly N times yielding an O(N) time complexity. Using list appending instead of string concatenation ensures O(N) performance rather than decaying into O(N^2).",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Single-Space Title Casing",
                "scenario": "Write a function that accepts a string of purely lowercase words separated by exactly one space, and returns the string in Title Case. The first letter of each word must be capitalized. You may **not** use Python's built-in `.title()` method.",
                "hint": "You can process the string character by character. Use a boolean variable (like `is_new_word`) that starts as `True`, and toggle it when you hit a space character.",
                "data": pd.DataFrame({
                    "string": ["hello world", "python", "data engineering"]
                }),
                "evaluation_criteria": [
                    "Ability to implement a basic state-machine loop over a string.",
                    "Handling string concatenation or appending to a list efficiently."
                ],
                "solution_code": """\
def manual_title_case(s):
    result = []
    new_word = True
    
    for char in s:
        if char == ' ':
            result.append(char)
            new_word = True
        elif new_word:
            result.append(char.upper())
            new_word = False
        else:
            result.append(char)
            
    return "".join(result)

df["title_cased"] = df["string"].apply(manual_title_case)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["hello world", "python", "data engineering"],
                    "title_cased": ["Hello World", "Python", "Data Engineering"]
                }),
                "follow_up_probes": [
                    "Performance: Why do we append to a list and use `\"\".join(result)` instead of doing `result_string += char` in the loop?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Mixed Case Inputs",
                "scenario": "Now assume the input strings can have mixed upper and lower casing (e.g., \"pYTHON\"). Your function must ensure that inside a word, only the first letter is capitalized, and the rest are explicitly lowercased.",
                "hint": "You'll need an `else` branch in your logic when you're inside a word but NOT at the first character.",
                "data": pd.DataFrame({
                    "string": ["hello world", "pYTHON", "dAtA EnGiNeErInG"]
                }),
                "evaluation_criteria": [
                    "Modifying conditional iteration to selectively transform characters based on their position in a word.",
                    "Gracefully building upon the existing state-machine."
                ],
                "solution_code": """\
def manual_title_case(s):
    result = []
    if not s: return ""
    
    new_word = True
    
    for char in s:
        if char == ' ':
            result.append(char)
            new_word = True
        elif new_word:
            result.append(char.upper())
            new_word = False
        else:
            result.append(char.lower())
            
    return "".join(result)

df["title_cased"] = df["string"].apply(manual_title_case)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["hello world", "pYTHON", "dAtA EnGiNeErInG"],
                    "title_cased": ["Hello World", "Python", "Data Engineering"]
                }),
                "follow_up_probes": [
                    "Edge Cases: Does your code handle an entirely empty string correctly?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Multiple and Irregular Spaces",
                "scenario": "Real-world data is messy. Your function needs to handle multiple consecutive spaces, leading/trailing spaces, and even tabs or newlines. The exact whitespace structure must be preserved in the output string.",
                "hint": "Instead of explicitly checking against `' '`, Python has a built-in string method to check if a character is *any* kind of whitespace.",
                "data": pd.DataFrame({
                    "string": ["hello world", "pYTHON", "  spaces   everywhere  ", "\ttabs\nand spaces "]
                }),
                "evaluation_criteria": [
                    "Handling arbitrary whitespace sequences correctly without breaking tokenization boundaries.",
                    "Knowledge of character evaluation methods like `.isspace()`."
                ],
                "solution_code": """\
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
                "expected_output": pd.DataFrame({
                    "string": ["hello world", "pYTHON", "  spaces   everywhere  ", "\ttabs\nand spaces "],
                    "title_cased": ["Hello World", "Python", "  Spaces   Everywhere  ", "\tTabs\nAnd Spaces "]
                }),
                "follow_up_probes": [
                    "Built-in method limits: Why are we writing this manually instead of just using Python's built-in `.title()` method?",
                    "Space complexity: Can this be done with strictly O(1) extra space outside the returned string?"
                ]
            }
        ]
    }
