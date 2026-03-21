import pandas as pd

def get_exercise():
    return {
        "title": "Roman to Int",
        "subtitle": "Loops, Hash Maps / Dictionaries",
        "description": "Convert a Roman numeral string to an integer. Roman numerals are standard (I, V, X, L, C, D, M). Subtraction rules apply (e.g., IX is 9, XL is 40).",
        "data": pd.DataFrame({
            "roman": ["III", "LVIII", "MCMXCIV", "IV"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Create a dictionary mapping each Roman numeral character to its integer value. Iterate through the string from left to right. If the current character is smaller than the *next* character, subtract its value; otherwise, add it.",
        "hint_sql": "Not applicable",
        "solution_python": """
def roman_to_int(s):
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    # Store length to avoid calculating inside loop
    n = len(s)
    
    for i in range(n):
        value = roman_map[s[i]]
        # If we are not at the final character and the current value is less 
        # than the next value, it's a subtractive notation (e.g., IV)
        if i < n - 1 and value < roman_map[s[i+1]]:
            total -= value
        else:
            total += value
            
    return total

df["integer_value"] = df["roman"].apply(roman_to_int)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "Dictionary lookups in Python are O(1). The algorithm iterates through the string exactly once, giving an O(N) time complexity where N is the length of the string. The space complexity is O(1) because the mapping dictionary is a constant size (7 characters) regardless of the input.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Additive Numerals",
                "scenario": "Let's start with basic Roman numerals where each symbol is simply added to the total. There are no subtractive combinations like 'IV' or 'IX' yet. Convert the column of Roman numeral strings to integers.",
                "hint": "Create a dictionary mapping each character to its integer value. Loop through the string and add each character's value to a running total.",
                "data": pd.DataFrame({
                    "roman": ["III", "VI", "LX", "MD"]
                }),
                "evaluation_criteria": [
                    "Using a dictionary mapping for O(1) character lookups.",
                    "Basic loop structure and accumulation.",
                    "Using pandas `.apply()` for row-wise transformation."
                ],
                "solution_code": """\
def roman_to_int(s):
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for char in s:
        total += roman_map[char]
    return total

df["integer_value"] = df["roman"].apply(roman_to_int)
result = df
""",
                "expected_output": pd.DataFrame({
                    "roman": ["III", "VI", "LX", "MD"],
                    "integer_value": [3, 6, 60, 1500]
                }),
                "follow_up_probes": [
                    "Complexity: What is the Time and Space complexity of your solution?",
                    "Dictionary Creation: Does creating the dictionary inside the function affect performance? Where else could you place it?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Subtractive Rules",
                "scenario": "Great. Now let's introduce the subtractive rules. In standard Roman numerals, a smaller value placed immediately before a larger value means subtraction (e.g., 'IV' is 4, 'IX' is 9). Update your logic to handle this while continuing to support the additive cases.",
                "hint": "You'll need to look ahead to the next character in the string. If the current character's value is less than the next character's value, you subtract it instead of adding it.",
                "data": pd.DataFrame({
                    "roman": ["III", "IV", "IX", "LVIII", "MCMXCIV"]
                }),
                "evaluation_criteria": [
                    "Checking array bounds to avoid `IndexError`.",
                    "Logic for comparing current and next values.",
                    "Combining logic that works for both scenarios concurrently."
                ],
                "solution_code": """\
def roman_to_int(s):
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    n = len(s)
    
    for i in range(n):
        value = roman_map[s[i]]
        # Check bounds and subtractive rule
        if i < n - 1 and value < roman_map[s[i+1]]:
            total -= value
        else:
            total += value
            
    return total

df["integer_value"] = df["roman"].apply(roman_to_int)
result = df
""",
                "expected_output": pd.DataFrame({
                    "roman": ["III", "IV", "IX", "LVIII", "MCMXCIV"],
                    "integer_value": [3, 4, 9, 58, 1994]
                }),
                "follow_up_probes": [
                    "Loop Optimization: How does calculating `len(s)` once outside the loop compare to doing it inside the `range()` call?",
                    "Alternative Approaches: Could you do this by replacing substrings first (e.g., `s.replace('IV', 'IIII')`)? What are the tradeoffs?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Validation & Error Handling",
                "scenario": "Finally, our incoming production data might be messy. Some rows might contain invalid characters, numbers, or be entirely empty. Let's make the function robust. If a string contains invalid Roman numeral characters or is empty/null, return `0`.",
                "hint": "Ensure you handle types safely before iteration. You'll need to check if each character exists in your map and fail gracefully rather than throwing a KeyError.",
                "data": pd.DataFrame({
                    "roman": ["MCMXCIV", "IV", "A", "IIB", " ", None, 123]
                }),
                "evaluation_criteria": [
                    "Defensive type casting and null checks.",
                    "Handling unexpected input lengths gracefully.",
                    "Checking keys against a dictionary safely."
                ],
                "solution_code": """\
def roman_to_int(s):
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    
    # Cast to string and strip whitespace
    s_str = str(s).strip()
    
    # Explicitly check for empty or "None" values
    if not s_str or s_str == "None":
        return 0
        
    n = len(s_str)
    for i in range(n):
        char = s_str[i]
        
        # Validate character
        if char not in roman_map:
            return 0
            
        value = roman_map[char]
        
        # Safe lookahead with validation
        if i < n - 1 and s_str[i+1] in roman_map and value < roman_map[s_str[i+1]]:
            total -= value
        else:
            total += value
            
    return total

df["integer_value"] = df["roman"].apply(roman_to_int)
result = df
""",
                "expected_output": pd.DataFrame({
                    "roman": ["MCMXCIV", "IV", "A", "IIB", " ", None, 123],
                    "integer_value": [1994, 4, 0, 0, 0, 0, 0]
                }),
                "follow_up_probes": [
                    "Validation Design: Do you think silently returning `0` is better than raising an exception here? Why or why not in a data pipeline context?",
                    "Strictness: This code allows invalid combinations like 'IIII' or 'VX'. How much harder would it be to validate strict standard Roman numeral syntax?"
                ]
            }
        ]
    }
