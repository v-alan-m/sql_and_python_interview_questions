import pandas as pd

def get_exercise():
    return {
        "title": "Valid Parentheses",
        "description": "Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. Open brackets must be closed by the same type of brackets, and they must be closed in the correct order.",
        "data": pd.DataFrame({
            "string": ["()", "()[]{}", "(]", "([)]", "{[]}"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Use a Stack data structure (a Python list works perfectly using `.append()` and `.pop()`). When you see an opening bracket, push it to the stack. When you see a closing bracket, pop from the stack and ensure they form a matching pair.",
        "hint_sql": "Not applicable",
        "solution_python": """
def is_valid_parentheses(s):
    stack = []
    # Mapping of closing brackets to their corresponding opening brackets
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping.values():
            # If it's an opening bracket, push to stack
            stack.append(char)
        elif char in mapping.keys():
            # If it's a closing bracket
            if not stack:
                return False
            top_element = stack.pop()
            if mapping[char] != top_element:
                return False
        else:
            # Ignore non-bracket characters if any exist
            continue
            
    # Stack must be empty at the end for it to be valid
    return len(stack) == 0

df["is_valid"] = df["string"].apply(is_valid_parentheses)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "This is the classic Stack algorithmic problem. Because we process each character exactly once and stack operations (append/pop) are O(1), the time complexity is strictly linear O(N). Space complexity is O(N) in the worst case where the string is composed entirely of opening brackets e.g. '((((((', leading to all characters being pushed to the stack."
    }
