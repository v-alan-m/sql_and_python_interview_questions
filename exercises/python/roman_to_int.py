import pandas as pd

def get_exercise():
    return {
        "title": "Roman to Int",
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
        "deep_dive": "Dictionary lookups in Python are O(1). The algorithm iterates through the string exactly once, giving an O(N) time complexity where N is the length of the string. The space complexity is O(1) because the mapping dictionary is a constant size (7 characters) regardless of the input."
    }
