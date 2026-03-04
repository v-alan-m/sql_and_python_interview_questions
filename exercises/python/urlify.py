import pandas as pd

def get_exercise():
    return {
        "title": "URLify",
        "description": "Write a method to replace all spaces in a string with '%20'. You may assume that the string has sufficient space at the end to hold the additional characters, and that you are given the 'true' length of the string.",
        "data": pd.DataFrame({
            "string": ["Mr John Smith    ", "hello world  "],
            "true_length": [13, 11]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Normally in Python, you just use `.replace(' ', '%20')`. But to demonstrate algorithmic thinking (like in C or Java), you can convert the string to a character array (list), use two pointers starting from the end, and mutate the list in place.",
        "hint_sql": "Not applicable",
        "solution_python": """
def urlify(s, true_length):
    # The 'Pythonic' way:
    # return s[:true_length].replace(' ', '%20')
    
    # The Algorithmic (in-place list mutation) way:
    s_list = list(s)
    # Pointer to the end of the full string length (including space for %20)
    index = len(s) - 1
    
    # Iterate backwards from true_length
    for i in range(true_length - 1, -1, -1):
        if s_list[i] == ' ':
            s_list[index] = '0'
            s_list[index - 1] = '2'
            s_list[index - 2] = '%'
            index -= 3
        else:
            s_list[index] = s_list[i]
            index -= 1
            
    return "".join(s_list)

df["urlified"] = df.apply(lambda row: urlify(row["string"], row["true_length"]), axis=1)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "In lower-level languages, mutating strings in place backwards prevents overwriting characters before they are processed. This runs in O(N) time with O(1) extra space (assuming the string array itself has the buffer). In Python, since strings are immutable, we convert it to a list first, making the space complexity O(N). The Pythonic `.replace()` method is heavily optimized in C and is preferred in production Python code."
    }
