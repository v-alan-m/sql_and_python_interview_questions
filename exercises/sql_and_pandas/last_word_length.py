import pandas as pd

def get_exercise():
    return {
        "title": "Last Word Length",
        "description": "Given a string `s` consisting of words and spaces, return the length of the last word in the string. A word is a maximal substring consisting of non-space characters only.",
        "data": pd.DataFrame({
            "string": ["Hello World", "   fly me   to   the moon  ", "luffy is still joyboy"]
        }),
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
FROM table_name;
""",
        "deep_dive": "Python makes tokenization incredibly easy; `.split()` is an internal O(N) C-implementation that perfectly handles variable length whitespace natively. Doing string parsing backwards conceptually (without creating an array of strings first) is standard in SQL or lower-level languages like C to avoid massive memory allocations or when arrays aren't natively supported."
    }
