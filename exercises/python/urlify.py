import pandas as pd

def get_exercise():
    return {
        "title": "URLify",
        "subtitle": "Loops, Arrays / Lists, Two Pointers",
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
        "deep_dive": "In lower-level languages, mutating strings in place backwards prevents overwriting characters before they are processed. This runs in O(N) time with O(1) extra space (assuming the string array itself has the buffer). In Python, since strings are immutable, we convert it to a list first, making the space complexity O(N). The Pythonic `.replace()` method is heavily optimized in C and is preferred in production Python code.",
        "big_o_explanation": "### ⏱️ Optimal Big O Notation\n**Time Complexity:** `O(N)` where N is the length of the string. We iterate through the string a constant number of times.\n**Space Complexity:** `O(1)` auxiliary space if done in place (like in C/Java where the input buffer is modifiable). In Python, strings are immutable, so converting it to a list first requires `O(N)` space. The optimal algorithmic approach modifies the array in-place from back to front, avoiding shifting elements.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "The Built-in Pythonic Approach",
                "scenario": "Write a method to replace all spaces in a string with `'%20'`. You are given the string and its \"true\" length (the length of the string without any trailing buffer spaces). For this first stage, the interviewer just wants to see if you know the standard library. Implement this using Python's built-in string methods.",
                "hint": "You can slice the string to its `true_length` and then use string replacement.",
                "data": pd.DataFrame({
                    "string": ["Mr John Smith    ", "hello world  ", "python", "a b  "],
                    "true_length": [13, 11, 6, 3]
                }),
                "evaluation_criteria": [
                    "Knowledge of Python's string slicing (`s[:length]`).",
                    "Familiarity with the `.replace()` method."
                ],
                "solution_code": """\
def urlify(s, true_length):
    # Slice to true length and replace
    return s[:true_length].replace(' ', '%20')

df["urlified"] = df.apply(lambda row: urlify(row["string"], row["true_length"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["Mr John Smith    ", "hello world  ", "python", "a b  "],
                    "true_length": [13, 11, 6, 3],
                    "urlified": ["Mr%20John%20Smith", "hello%20world", "python", "a%20b"]
                }),
                "follow_up_probes": [
                    "Performance limits: Under the hood, how does `.replace()` manage memory?"
                ],
                "big_o_explanation": "#### Stage 1: Built-in string methods\n**Time Complexity:** `O(N)` since `.replace()` internally scans the string. Python's built-in methods are implemented in highly-optimized C code.\n**Space Complexity:** `O(N)` because a completely new string is allocated in memory to hold the replaced version. Strings in Python are immutable, so modifications always require new allocations."
            },
            {
                "stage_number": 2,
                "title": "Forward Array Building",
                "scenario": "The interviewer restricts you from using `.replace()`. They want to see how you would manually process the characters. Build a new string character by character by iterating forward up to `true_length`, substituting spaces as you go.",
                "hint": "Create a new empty list. Iterate through the string from index `0` to `true_length - 1`, appending characters or the `%20` sequence.",
                "data": pd.DataFrame({
                    "string": ["Mr John Smith    ", "hello world  ", "python", "a b  "],
                    "true_length": [13, 11, 6, 3]
                }),
                "evaluation_criteria": [
                    "Manual iteration through string indices.",
                    "Efficiently building a string using list appending rather than loop concatenation."
                ],
                "solution_code": """\
def urlify(s, true_length):
    result = []
    
    for i in range(true_length):
        if s[i] == ' ':
            result.append('%20')
        else:
            result.append(s[i])
            
    return "".join(result)

df["urlified"] = df.apply(lambda row: urlify(row["string"], row["true_length"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["Mr John Smith    ", "hello world  ", "python", "a b  "],
                    "true_length": [13, 11, 6, 3],
                    "urlified": ["Mr%20John%20Smith", "hello%20world", "python", "a%20b"]
                }),
                "follow_up_probes": [
                    "Space Complexity: What is the space complexity of this approach?"
                ],
                "big_o_explanation": "#### Stage 2: Forward Array Building\n**Time Complexity:** `O(N)`. We iterate through the original array exactly once from start to finish.\n**Space Complexity:** `O(N)`. We instantiate an auxiliary list `result` to hold the characters and the `%20` expansions, and then call `\"\".join(result)` to build the final string, requiring additional memory proportional to the size of the final string."
            },
            {
                "stage_number": 3,
                "title": "Optimal Backwards In-Place Traversal",
                "scenario": "In lower-level languages like C or Java, allocating completely new arrays can be costly. The input string actually has extra buffer spaces at the end designed to hold the extra characters from `%20`. Mutate the array *in-place* to achieve O(1) auxiliary space.",
                "hint": "If you iterate forwards and mutate in place, you'll overwrite characters you haven't processed yet. Try iterating *backwards* from `true_length - 1` while keeping a second pointer at the very end of the full array buffer.",
                "data": pd.DataFrame({
                    "string": ["Mr John Smith    ", "hello world  ", "python", "a b  "],
                    "true_length": [13, 11, 6, 3]
                }),
                "evaluation_criteria": [
                    "Recognizing the \"overwrite\" risk of forward in-place modification.",
                    "Using two-pointer technique for backwards array shifting."
                ],
                "solution_code": """\
def urlify(s, true_length):
    s_list = list(s)
    # Pointer to the end of the full buffer string length
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
                "expected_output": pd.DataFrame({
                    "string": ["Mr John Smith    ", "hello world  ", "python", "a b  "],
                    "true_length": [13, 11, 6, 3],
                    "urlified": ["Mr%20John%20Smith", "hello%20world", "python", "a%20b"]
                }),
                "follow_up_probes": [
                    "Pointer Math: Why do we subtract 3 from the `index` when a space is found, but only subtract 1 for regular characters?",
                    "Real-world Application: In actual Python development, which of these 3 stages would you merge into production codebase?"
                ],
                "big_o_explanation": "#### Stage 3: Optimal Backwards In-Place Traversal\n**Time Complexity:** `O(N)`. We iterate backwards from the original `true_length` to index 0.\n**Space Complexity:** `O(1)` auxiliary space theoretically, assuming the array is already sized to hold the extra characters and we are mutating the array directly (as we would in C/C++). In Python, we start by doing `list(s)` which takes `O(N)` space initially due to immutability, but the actual algorithmic operation (the two-pointer technique) avoids allocating any *new* auxiliary arrays during the traversal."
            }
        ]
    }
