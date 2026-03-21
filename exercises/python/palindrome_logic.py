import pandas as pd

def get_exercise():
    return {
        "title": "Palindrome Logic",
        "subtitle": "Loops, Arrays / Lists, Two Pointers",
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
        "deep_dive": "Creating the cleaned list of characters takes O(N) time and O(N) space. Reversing the list and comparing it also takes O(N) time and requires another O(N) space. For extreme memory constraints, a two-pointer approach (one pointer at the start, one at the end, iterating inward and skipping non-alphanumeric chars) can achieve O(N) time and O(1) extra space.",
        "big_o_explanation": "Time Complexity: O(N) where N is the length of the string. Creating the cleaned list and reversing it both require a full pass over the characters. Space Complexity: O(N) since we allocate a new list `cleaned` and a sliced reversed list `cleaned[::-1]`. A two-pointer approach could reduce the space complexity to O(1) by skipping non-alphanumeric characters in-place.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Strings",
                "scenario": "Verify if a given string is a palindrome (reads the same forwards and backwards). Assume the input strings only contain lowercase alphabetic characters and no spaces.",
                "hint": "You can easily reverse a string (or a list) in Python using slicing with a step of `-1` (e.g., `s[::-1]`). Compare the original string to the reversed one.",
                "data": pd.DataFrame({
                    "string": [
                        "racecar", 
                        "hello", 
                        "madam", 
                        "python"
                    ]
                }),
                "evaluation_criteria": [
                    "Simple string manipulation and comparison.",
                    "Knowledge of Python's slicing mechanics."
                ],
                "solution_code": """\
def is_palindrome(s):
    return s == s[::-1]

df["is_palindrome"] = df["string"].apply(is_palindrome)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": [
                        "racecar", 
                        "hello", 
                        "madam", 
                        "python"
                    ],
                    "is_palindrome": [True, False, True, False]
                }),
                "big_o_explanation": "Time Complexity: O(N) to traverse the string of length N for reversing and checking equality. Space Complexity: O(N) because the slice `[::-1]` allocates a completely new string in memory. While computationally efficient, this is not optimal for extreme memory constraints compared to an in-place two-pointer approach.",
                "follow_up_probes": [
                    "Time Complexity: What is the time and space complexity of string slicing in Python? (O(N) time and O(N) space to create the new string).",
                    "Alternative Approaches: How would you do this without slicing or creating a new string, using only O(1) extra space? (Using two pointers from opposite ends)."
                ]
            },
            {
                "stage_number": 2,
                "title": "Case & Spaces",
                "scenario": "Now the input strings can contain spaces and mixed capitalisation. You need to ignore spaces and make the comparison case-insensitive.",
                "hint": "Use `.lower()` to handle case sensitivity. You can iterate through the characters and assemble a new list or string filtering out explicit space characters `' '`.",
                "data": pd.DataFrame({
                    "string": [
                        "Race car", 
                        "hello", 
                        "Madam", 
                        "python code"
                    ]
                }),
                "evaluation_criteria": [
                    "String methods (`.lower()`).",
                    "Filtering logic using list comprehensions or standard loops.",
                    "Mixing old test case logic (already contiguous lowercase) with new logic."
                ],
                "solution_code": """\
def is_palindrome_spaces(s):
    cleaned = [c.lower() for c in s if c != ' ']
    return cleaned == cleaned[::-1]

df["is_palindrome"] = df["string"].apply(is_palindrome_spaces)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": [
                        "Race car", 
                        "hello", 
                        "Madam", 
                        "python code"
                    ],
                    "is_palindrome": [True, False, True, False]
                }),
                "big_o_explanation": "Time Complexity: O(N) where N is the length of the string. The list comprehension iterates through all N characters, and reversing/comparing the list also takes O(N) time. Space Complexity: O(N) because we build a new list `cleaned` to store the valid lowercase characters, plus another O(N) for the reversed list. Using `.lower()` on each character individually inside the loop is slightly slower than lowering the entire string upfront but still O(N).",
                "follow_up_probes": [
                    "String Construction vs Lists: Why build a list of characters and compare those, rather than using string concatenation (`+=`)? (Strings are immutable so `+=` rebuilds the string every iteration taking O(N^2) time, whereas a list comprehension is O(N))."
                ]
            },
            {
                "stage_number": 3,
                "title": "Alphanumeric & Punctuation",
                "scenario": "The input can now contain full sentences with punctuation, numbers, and special characters. Verify if it's a palindrome, considering *only* alphanumeric characters and ignoring everything else.",
                "hint": "Python strings have built-in methods to check for character types. Look into `.isalnum()`.",
                "data": pd.DataFrame({
                    "string": [
                        "A man, a plan, a canal: Panama", 
                        "race a car", 
                        "racecar",
                        "Race car",
                        " ", 
                        "No 'x' in Nixon"
                    ]
                }),
                "evaluation_criteria": [
                    "Usage of the `.isalnum()` built-in method (or regex/ascii ranges).",
                    "Final robustness on all edge cases."
                ],
                "solution_code": """\
def is_palindrome_alnum(s):
    # Filter alphanumeric & convert to lowercase
    cleaned = [char.lower() for char in s if char.isalnum()]
    
    # Check if string matches its reverse
    return cleaned == cleaned[::-1]

df["is_palindrome"] = df["string"].apply(is_palindrome_alnum)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": [
                        "A man, a plan, a canal: Panama", 
                        "race a car", 
                        "racecar",
                        "Race car",
                        " ", 
                        "No 'x' in Nixon"
                    ],
                    "is_palindrome": [True, False, True, True, True, True]
                }),
                "big_o_explanation": "Time Complexity: O(N) because we evaluate `.isalnum()` and `.lower()` for each character, followed by a reverse and compare operation. Space Complexity: O(N) due to the list comprehension creating the `cleaned` character list. While optimal time-wise, the extra memory allocation can be avoided entirely in memory-constrained environments by using a two-pointer approach that evaluates `.isalnum()` on the fly from the ends inward.",
                "follow_up_probes": [
                    "Empty Spaces Context: Look at the row containing `\" \"`. The cleaned structure became empty `[]`, yet the output is `True`. Why does an empty string/list equal a reversed empty list?",
                    "Two Pointers Complexity: If you converted this logic to a two-pointer approach, what happens when a pointer lands on punctuation? (You increment/decrement that pointer until it hits an alphanumeric char, keeping memory strictly O(1))."
                ]
            }
        ]
    }
