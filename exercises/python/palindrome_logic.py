import pandas as pd

def get_exercise():
    return {
        "title": "Palindrome Logic",
        "description": "Given a string, verify if it is a palindrome. Consider only alphanumeric characters and ignore case (e.g., 'A man, a plan, a canal: Panama' is a palindrome).",
        "data": pd.DataFrame({
            "string": [
                "A man, a plan, a canal: Panama", 
                "race a car", 
                " ", 
                "No 'x' in Nixon"
            ]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "First, filter out any non-alphanumeric characters and convert the string to lowercase. You can use `.isalnum()` for filtering. Then check if the cleaned string reads the same forwards and backwards using slicing `[::-1]` or two pointers.",
        "hint_sql": "Not applicable",
        "solution_python": """
def is_palindrome(s):
    # Filter alphanumeric & convert to lowercase
    cleaned = [char.lower() for char in s if char.isalnum()]
    
    # Check if string matches its reverse
    return cleaned == cleaned[::-1]

df["is_palindrome"] = df["string"].apply(is_palindrome)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "Creating the cleaned list of characters takes O(N) time and O(N) space. Reversing the list and comparing it also takes O(N) time and requires another O(N) space. For extreme memory constraints, a two-pointer approach (one pointer at the start, one at the end, iterating inward and skipping non-alphanumeric chars) can achieve O(N) time and O(1) extra space."
    }
