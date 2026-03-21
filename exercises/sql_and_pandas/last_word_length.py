import pandas as pd

def get_exercise():
    return {
        "title": "Last Word Length",
        "description": "Given a string `s` consisting of words and spaces, return the length of the last word in the string. A word is a maximal substring consisting of non-space characters only.",
        "data": pd.DataFrame({
            "string": ["Hello World", "   fly me   to   the moon  ", "luffy is still joyboy"]
        }),
        "table_name": "text_data",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "The `.split()` method in Python handles trailing whitespaces automatically if used without arguments. Alternatively, `.strip()` the string first.",
        "hint_sql": "SQL string manipulation varies by dialect. You typically need to `TRIM()` trailing spaces first, then find the position of the last space using `REVERSE()` and `CHARINDEX()` or `STRPOS()`. The difference is the last word length.",
        "solution_python": """
def get_last_word_length(s):
    # .strip() removes leading and trailing whitespace
    # .split(' ') splits strictly by space
    # words = s.strip().split(' ')
    # return len(words[-1])
    
    # Even simpler: .split() with no args handles all contiguous whitespace
    words = s.split()
    return len(words[-1]) if words else 0

df["last_word_length"] = df["string"].apply(get_last_word_length)
result = df
""",
        "solution_sql": """
-- Example for PostgreSQL / standard SQL functions
-- 1. Trim trailing spaces
-- 2. Reverse the trimmed string so the target word is at the beginning
-- 3. Find the position of the first space in the reversed string
-- 4. If there's no space, the whole trimmed string is the word. Else, it's the index - 1.

SELECT 
    string,
    CASE 
        WHEN POSITION(' ' IN REVERSE(TRIM(string))) = 0 
        THEN LENGTH(TRIM(string))
        ELSE POSITION(' ' IN REVERSE(TRIM(string))) - 1
    END AS last_word_length
FROM text_data;
""",
        "deep_dive": "Python makes tokenization incredibly easy; `.split()` is an internal O(N) C-implementation that perfectly handles variable length whitespace natively. Doing string parsing backwards conceptually (without creating an array of strings first) is standard in SQL or lower-level languages like C to avoid massive memory allocations or when arrays aren't natively supported.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Single Word Evaluation",
                "scenario": "Calculate the length of the string, assuming it contains exactly one word without any spaces.",
                "hint": "In Python, use `len()`. In SQL, use `LENGTH()`.",
                "data": pd.DataFrame({
                    "string": ["Hello", "world", "Python"]
                }),
                "evaluation_criteria": [
                    "Basic string length calculation."
                ],
                "solution_code": """\
def get_last_word_length(s):
    return len(s)

df["last_word_length"] = df["string"].apply(get_last_word_length)
result = df
""",
                "solution_sql": """\
SELECT 
    string,
    LENGTH(string) AS last_word_length
FROM text_data;
""",
                "expected_output": pd.DataFrame({
                    "string": ["Hello", "world", "Python"],
                    "last_word_length": [5, 5, 6]
                }),
                "follow_up_probes": [
                    "What is the time complexity of the length function in Python?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Clean Sentence",
                "scenario": "The string now contains multiple words separated by single spaces. There are no leading or trailing spaces. Find the length of the last word.",
                "hint": "In Python, split the string by space and take the last element. In SQL, you can reverse the string and find the first space.",
                "data": pd.DataFrame({
                    "string": ["Hello World", "Data Engineering", "SQL and Python", "Python"]
                }),
                "evaluation_criteria": [
                    "Splitting strings into arrays/lists.",
                    "Accessing the last element.",
                    "SQL string manipulation functions (REVERSE, POSITION)."
                ],
                "solution_code": """\
def get_last_word_length(s):
    words = s.split(' ')
    return len(words[-1])

df["last_word_length"] = df["string"].apply(get_last_word_length)
result = df
""",
                "solution_sql": """\
SELECT 
    string,
    CASE 
        WHEN POSITION(' ' IN REVERSE(string)) = 0 THEN LENGTH(string)
        ELSE POSITION(' ' IN REVERSE(string)) - 1
    END AS last_word_length
FROM text_data;
""",
                "expected_output": pd.DataFrame({
                    "string": ["Hello World", "Data Engineering", "SQL and Python", "Python"],
                    "last_word_length": [5, 11, 6, 6]
                }),
                "follow_up_probes": [
                    "How does splitting the entire string affect memory usage if the string is extremely large?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Messy Spacing",
                "scenario": "The input string may contain leading spaces, trailing spaces, and multiple spaces between words. Return the length of the last non-space word.",
                "hint": "In Python, consider how `.split()` behaves with and without arguments, or use `.strip()`. In SQL, use `TRIM()`.",
                "data": pd.DataFrame({
                    "string": ["Hello World", "   fly me   to   the moon  ", "luffy is still joyboy", "   a   "]
                }),
                "evaluation_criteria": [
                    "Robust whitespace handling.",
                    "Python's default `split()` behavior.",
                    "SQL `TRIM()` function."
                ],
                "solution_code": """\
def get_last_word_length(s):
    words = s.split()
    return len(words[-1]) if words else 0

df["last_word_length"] = df["string"].apply(get_last_word_length)
result = df
""",
                "solution_sql": """\
SELECT 
    string,
    CASE 
        WHEN POSITION(' ' IN REVERSE(TRIM(string))) = 0 THEN LENGTH(TRIM(string))
        ELSE POSITION(' ' IN REVERSE(TRIM(string))) - 1
    END AS last_word_length
FROM text_data;
""",
                "expected_output": pd.DataFrame({
                    "string": ["Hello World", "   fly me   to   the moon  ", "luffy is still joyboy", "   a   "],
                    "last_word_length": [5, 4, 6, 1]
                }),
                "follow_up_probes": [
                    "Can you solve this in Python without creating a new list of words?",
                    "What is the time complexity of reversing the string in SQL and is there an alternative?"
                ]
            }
        ]
    }
