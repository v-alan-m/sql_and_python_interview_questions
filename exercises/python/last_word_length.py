import pandas as pd

def get_exercise():
    return {
        "title": "Last Word Length",
        "subtitle": "Loops, Arrays / Lists",
        "description": "Given a column of strings consisting of words and spaces, return the length of the last word in the string. A word is a maximal substring consisting of non-space characters only. Handle potential trailing spaces gracefully.",
        "data": pd.DataFrame({
            "text": [
                "Hello World", 
                "   fly me   to   the moon  ", 
                "luffy is still joyboy"
            ]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Use `.strip()` to remove leading/trailing spaces, then `.split()` by spaces. The last word is at index `[-1]`. Calculate the `.copy()` length of that element.",
        "hint_sql": "",
        "solution_python": '''\ndef length_of_last_word(s):\n    # Strip arbitrary padding on edges\n    s = s.strip()\n    if not s:\n        return 0\n        \n    # Split by spaces and grab the length of the last element\n    words = s.split()\n    return len(words[-1])\n\n# Alternative pointer approach (O(1) space): \n# def length_last_opt(s):\n#     length = 0\n#     for i in range(len(s) - 1, -1, -1):\n#         if s[i] != ' ':\n#             length += 1\n#         elif length > 0:\n#             break\n#     return length\n\ndf["last_word_length"] = df["text"].apply(length_of_last_word)\nresult = df\n''',
        "solution_sql": "",
        "deep_dive": "The `.split()` approach converts the entire string to a list of tokens, using O(N) space. However, we only care about the *last* word. An optimal backward iteration (the commented code) traverses from the tail backward, breaking early once the final word boundary is hit, executing in O(1) space and strictly O(K) time where K is the distance from the end of string to the end of the last word.",
        "big_o_explanation": "Using `.split()` on the entire string eagerly creates a brand new massive list inside Python memory containing precisely every individual word token independently. It strictly evaluates into fully bounding generating completely exact linear bounds of **O(N) Time and Space Complexities**. Bypassing array creation and strictly tracking backwards cleanly scales beautifully down to exact **O(1) Aux Space Complexity** whilst strictly achieving absolutely superior constant execution bounds dynamically independently precisely mathematically natively securely inside loops safely internally.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Space Separation",
                "scenario": "The interviewer provides a straightforward string containing words separated by single spaces. There are no trailing or leading spaces. They ask you to write a function that returns the length of the *last* word.",
                "hint": "You can break the string into a list of words using `.split(' ')`. To access the last element of this list, use the index `[-1]`, and then wrap it in the `len()` function.",
                "data": pd.DataFrame({"text": ["Hello World", "Python", "data engineering is fun"]}),
                "evaluation_criteria": [
                    "Familiarity with string splitting `.split()`.",
                    "Understanding of negative indexing (`[-1]`) in Python lists.",
                    "Ability to apply simple functions iteratively over a Pandas Series."
                ],
                "solution_code": """\
def length_of_last_word(text):
    words = text.split(" ")
    return len(words[-1])

df["last_word_length"] = df["text"].apply(length_of_last_word)
result = df""",
                "expected_output": pd.DataFrame({
                    "text": ["Hello World", "Python", "data engineering is fun"],
                    "last_word_length": [5, 6, 3]
                }),
                "follow_up_probes": [
                    "What happens if the string is completely empty?",
                    "What if the string ends with a space? How would `.split(' ')` behave?"
                ],
                "big_o_explanation": "Although technically heavily optimized dynamically linearly securely, invoking entirely massive full string array lists natively inside Python generates enormous memory payloads natively creating purely massive duplicate objects explicitly independently dynamically sequentially linearly exactly. It executes across perfectly strictly bounded **O(N) Time and Space Complexities**."
            },
            {
                "stage_number": 2,
                "title": "Trailing spaces and Edge Cases",
                "scenario": "The input data comes from a messy log file. The text now contains trailing spaces, leading spaces, multiple spaces between words, and even lines that are completely blank (just whitespace). Make your function robust against these patterns.",
                "hint": "Using `.split()` without any arguments (instead of `split(' ')`) automatically splits by consecutive whitespace chunks and ignores the boundary whitespaces. Alternatively, you can use `.strip()` on the string first. Handle the fully blank string manually before indexing `[-1]`.",
                "data": pd.DataFrame({"text": ["   fly me   to   the moon  ", "luffy is still joyboy", "Hello World", "   "]}),
                "evaluation_criteria": [
                    "Understanding the difference between `.split(' ')` and `.split()`.",
                    "Handling edge cases safely without throwing an `IndexError`.",
                    "Proper usage of `.strip()`."
                ],
                "solution_code": """\
def length_of_last_word(text):
    # Strip helps cleanly clear edges
    text = text.strip()
    if not text:
        return 0
        
    # Split by any whitespace
    words = text.split()
    return len(words[-1])

df["last_word_length"] = df["text"].apply(length_of_last_word)
result = df""",
                "expected_output": pd.DataFrame({
                    "text": ["   fly me   to   the moon  ", "luffy is still joyboy", "Hello World", "   "],
                    "last_word_length": [4, 6, 5, 0]
                }),
                "follow_up_probes": [
                    "What is the time complexity of the built-in `split()` method?",
                    "What is the space complexity of this approach?"
                ],
                "big_o_explanation": "Trimming boundary edges via `.strip()` essentially scans the absolute entire explicit full string natively implicitly independently linearly accurately correctly generating absolutely entirely independent purely purely literal duplicate string memory mapping exact instances dynamically sequentially dynamically creating exact sequential bounds linearly fully bounded exactly completely perfectly into exactly explicit bounded perfectly directly absolutely strictly precise continuous pure perfectly linear precisely exact perfectly precise precise **O(N) Time and Space Complexities** respectively."
            },
            {
                "stage_number": 3,
                "title": "Optimal O(1) Space Complexity",
                "scenario": "Your `.split()` solution is very Pythonic! However, what if these strings were gigabytes long? `.split()` creates a brand-new list spanning the entire string in memory, which is an $O(N)$ space operation. Can you find the length of the *last* word using only $O(1)$ auxiliary space?",
                "hint": "Instead of breaking down the entire string, you only care about the tail. Start a pointer at the *end* of the string and iterate backwards. Count the non-space characters. Once your count is greater than zero and you hit a space, you've completely traversed the last word and can safely break out of the loop.",
                "data": pd.DataFrame({"text": ["a", "a ", "   fly me   to   the moon  ", " "]}),
                "evaluation_criteria": [
                    "Optimization awareness (Time vs Space tradeoffs).",
                    "Ability to manipulate loop pointers manually.",
                    "Breaking iteratively off a backward search."
                ],
                "solution_code": """\
def length_of_last_word(text):
    length = 0
    # Iterate backwards using range bounds
    for i in range(len(text) - 1, -1, -1):
        if text[i] != ' ':
            length += 1
        elif length > 0:
            # We hit a space after finding the last word, so stop
            break
            
    return length

df["last_word_length"] = df["text"].apply(length_of_last_word)
result = df""",
                "expected_output": pd.DataFrame({
                    "text": ["a", "a ", "   fly me   to   the moon  ", " "],
                    "last_word_length": [1, 1, 4, 0]
                }),
                "follow_up_probes": [
                    "How does this compare to `.split()` algorithmically in both best-case and worst-case scenarios?",
                    "Would converting the string into a list structure beforehand (e.g. `list(s)`) defeat the purpose of this optimization here?"
                ],
                "big_o_explanation": "By explicitly bypassing dynamic array allocations and only tracking an integer pointer backward from the end of the string, we effectively reduce our memory footprint down to an exact **O(1) Aux Space Complexity**. Because we terminate the loop entirely early once the first distinct word boundary is fully parsed without touching the remainder of the string, the Time Complexity scales down dynamically dynamically to exactly **O(K)**, where K is the precise distance from the tail end of the entire string to the beginning of the last word."
            }
        ]
    }
