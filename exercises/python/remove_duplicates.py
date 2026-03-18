import pandas as pd

def get_exercise():
    return {
        "title": "Remove Duplicates",
        "description": "Given a text column, remove all consecutive duplicate characters from the string. For example, 'aabbcc' becomes 'abc', and 'mississippi' becomes 'misisipi'.",
        "data": pd.DataFrame({
            "text": [
                "aabbcc", 
                "mississippi", 
                "hello world",
                "a"
            ]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Iterate through the string and append characters to a new list only if the character is different from the last character added to that list.",
        "hint_sql": "",
        "solution_python": '''\ndef remove_consecutive_duplicates(text):\n    if not text:\n        return text\n        \n    result = [text[0]]\n    \n    for i in range(1, len(text)):\n        # Only append if it's different from the most recently added char\n        if text[i] != result[-1]:\n            result.append(text[i])\n            \n    return "".join(result)\n\ndf["deduped_text"] = df["text"].apply(remove_consecutive_duplicates)\nresult = df\n''',
        "solution_sql": "",
        "deep_dive": "This is a simple state-tracking algorithm. By using the end of the `result` list `result[-1]` as our state tracker, we avoid needing a separate variable to keep track of the 'previous' character. The time complexity is exactly O(N) because we iterate through the sequence precisely once, and list appends in Python are amortized O(1).",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Consecutive Characters",
                "scenario": "Given a text string, write a function that removes all consecutive duplicate characters. For example, 'aabbcc' becomes 'abc', and 'hello' becomes 'helo'. The string can contain multiple words.",
                "hint": "You don't need to keep track of characters seen globally — only the most recently added character. Try iterating through the string and appending characters to a result list only if they differ from the last character in the list.",
                "data": pd.DataFrame({
                    "text": ["aabbcc", "mississippi", "hello world", "a"]
                }),
                "evaluation_criteria": [
                    "Simple state tracking using a result list.",
                    "Handling edge cases (empty strings, single characters).",
                    "Efficient string building (using a list + `join()` rather than concatenating strings in a loop)."
                ],
                "solution_code": """\
def remove_consecutive_duplicates(text):
    if not text:
        return text
        
    result = [text[0]]
    
    for i in range(1, len(text)):
        # Only append if it's different from the most recently added char
        if text[i] != result[-1]:
            result.append(text[i])
            
    return "".join(result)

df["deduped_text"] = df["text"].apply(remove_consecutive_duplicates)
result = df
""",
                "expected_output": pd.DataFrame({
                    "text": ["aabbcc", "mississippi", "hello world", "a"],
                    "deduped_text": ["abc", "misisipi", "helo world", "a"]
                }),
                "follow_up_probes": [
                    "Time/Space Complexity: What is the time and space complexity of your solution?",
                    "String Immutability: Why did you use a list and `join()` instead of just doing `result_str += text[i]`?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Case-Insensitive Deduplication",
                "scenario": "Let's make it case-insensitive. If an uppercase 'E' follows a lowercase 'e', they should be treated as duplicates. However, you should preserve the case of the *first* character you encounter in that sequence. For example, 'HeEllo' should become 'Helo'.",
                "hint": "You can still compare the current character to the last character in your result list, but you'll need to convert both to lowercase before doing the comparison.",
                "data": pd.DataFrame({
                    "text": ["aAabbcc", "HeEllo World", "mississippi"]
                }),
                "evaluation_criteria": [
                    "String manipulation and case transformation methods (`.lower()`).",
                    "Ensuring the original case is appended to the result, not the lowercase version."
                ],
                "solution_code": """\
def remove_consecutive_duplicates(text):
    if not text:
        return text
        
    result = [text[0]]
    
    for i in range(1, len(text)):
        # Compare lowercase versions, but append the original character
        if text[i].lower() != result[-1].lower():
            result.append(text[i])
            
    return "".join(result)

df["deduped_text"] = df["text"].apply(remove_consecutive_duplicates)
result = df
""",
                "expected_output": pd.DataFrame({
                    "text": ["aAabbcc", "HeEllo World", "mississippi"],
                    "deduped_text": ["abc", "Helo World", "misisipi"]
                }),
                "follow_up_probes": [
                    "Two Pointers: Could this be done in-place if strings were mutable in our language (like C++)? How would the two-pointer approach work?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Selective Deduplication (Letters Only)",
                "scenario": "Now let's add a selective rule: we only want to deduplicate *alphabetic letters*. If there are consecutive spaces, punctuation marks, or numbers, they should be left exactly as they are. Letters should still be deduplicated case-insensitively.",
                "hint": "Before deciding whether to skip a character, first check if both the current character and the previous character are alphabetic (`.isalpha()`). If they aren't both letters, you should always append the current character.",
                "data": pd.DataFrame({
                    "text": ["hello... world!!!", "HeEllo World!!", "aAabbcc..."]
                }),
                "evaluation_criteria": [
                    "Conditional logic combining character property checks (`.isalpha()`) with equality checks.",
                    "Cleanly structuring complex boolean conditions without deep nesting."
                ],
                "solution_code": """\
def remove_consecutive_duplicates(text):
    if not text:
        return text
        
    result = [text[0]]
    
    for i in range(1, len(text)):
        curr = text[i]
        prev = result[-1]
        
        # Only deduplicate if both are letters and match case-insensitively
        if curr.isalpha() and prev.isalpha() and curr.lower() == prev.lower():
            continue
            
        result.append(curr)
            
    return "".join(result)

df["deduped_text"] = df["text"].apply(remove_consecutive_duplicates)
result = df
""",
                "expected_output": pd.DataFrame({
                    "text": ["hello... world!!!", "HeEllo World!!", "aAabbcc..."],
                    "deduped_text": ["helo... world!!!", "Helo World!!", "abc..."]
                }),
                "follow_up_probes": [
                    "Regular Expressions: If we wanted to solve this whole problem (Stage 3) using standard Regex substitution instead of a loop, what pattern would we use?"
                ]
            }
        ]
    }
