import pandas as pd

def get_exercise():
    return {
        "title": "String Compression",
        "subtitle": "Loops, Arrays / Lists",
        "description": "Implement a method to perform basic string compression using the counts of repeated characters. For example, the string 'aabcccccaaa' would become 'a2b1c5a3'. If the 'compressed' string would not become smaller than the original string, your method should return the original string. You can assume the string has only uppercase and lowercase letters (a - z).",
        "data": pd.DataFrame({
            "string": ["aabcccccaaa", "abcdef", "aabbcc", "wwwwwaaaaabbbbb"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Iterate through the string, keeping a count of consecutively repeating characters. When the character changes (or you reach the end), append the character and its count to a list. Finally, `.join()` the list and compare its length with the original string.",
        "hint_sql": "Not applicable",
        "solution_python": """
def compress_string(s):
    if not s:
        return ""
        
    compressed = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            compressed.append(s[i - 1] + str(count))
            count = 1
            
    # Add the last character and its count
    compressed.append(s[-1] + str(count))
    
    compressed_str = "".join(compressed)
    
    return compressed_str if len(compressed_str) < len(s) else s

df["compressed"] = df["string"].apply(compress_string)
result = df
""",
        "solution_sql": "Not applicable",
        "big_o_explanation": "Time Complexity: O(N) where N is the length of the string, tracking state via loop. List iteration and `\"\".join()` logic prevents O(N^2) breakdown in Python string manipulation. Space Complexity: O(N) to explicitly store both the dynamically constructed list tokens and the final string equivalent.",
        "deep_dive": "String concatenation in Python creates a new string each time, which can take O(N^2) time if done repeatedly. By appending to a list and then using `''.join()`, the algorithm runs in O(N) time complexity where N is the length of the string. The space complexity is also O(N) to store the compressed representation.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Character Grouping",
                "scenario": "Let's start by building the core compression logic. Write a function that takes a string and returns a compressed version where consecutive identical characters are replaced by the character and its count. Don't worry about the length constraint yet—just return the compressed version unconditionally.",
                "hint": "Iterate through the string from the second character. Compare each character to the previous one to keep a running count. When it changes, store the previous character and its count. Don't forget to handle the very last character group after the loop ends!",
                "data": pd.DataFrame({
                    "string": ["aaabbc", "zzzzzz", "aaxyz"]
                }),
                "evaluation_criteria": [
                    "Maintains a count correctly when comparing current and previous character.",
                    "Properly handles the state transition when the character changes.",
                    "Correctly adds the final counting block after the loop terminates.",
                    "Avoids out of bounds errors during iteration."
                ],
                "solution_code": """\
def compress_string(s):
    compressed = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            compressed.append(s[i - 1] + str(count))
            count = 1
            
    compressed.append(s[-1] + str(count))
    return "".join(compressed)

df["compressed"] = df["string"].apply(compress_string)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["aaabbc", "zzzzzz", "aaxyz"],
                    "compressed": ["a3b2c1", "z6", "a2x1y1z1"]
                }),
                "big_o_explanation": "Time Complexity: O(N). Iterating through every character natively executes linearly, while accessing `s[i - 1]` resolves memory in O(1) blocks. Space Complexity: O(N). If character variances are high (e.g. \"abcdef\"), the list scales to O(2N) size temporarily returning an O(N) envelope overall.",
                "follow_up_probes": [
                    "What is the time complexity of your approach? Why did you choose a list instead of concatenating strings directly?",
                    "What happens if we pass an empty string to your function right now?",
                    "Can you walk through your iteration exactly to show how the very last character gets processed?"
                ]
            },
            {
                "stage_number": 2,
                "title": "The Length Constraint",
                "scenario": "Great, the basic logic works. However, the goal of string compression is to save space! If the compressed version isn't strictly shorter than the original string, we shouldn't use it. Update your function to return the original string if the compressed string does not save any space.",
                "hint": "Keep your existing logic, but assign the joined compressed result to a variable. Compare its length to the length of the input string `s`. Return it only if `len(compressed_string) < len(s)`.",
                "data": pd.DataFrame({
                    "string": ["aabcccccaaa", "abcdef", "aabb", "aaabbc"]
                }),
                "evaluation_criteria": [
                    "Successfully implements the length check logic.",
                    "Does not disrupt the existing character grouping code.",
                    "Handles cases where lengths are exactly equal by appropriately returning the original string."
                ],
                "solution_code": """\
def compress_string(s):
    compressed = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            compressed.append(s[i - 1] + str(count))
            count = 1
            
    compressed.append(s[-1] + str(count))
    compressed_str = "".join(compressed)
    
    return compressed_str if len(compressed_str) < len(s) else s

df["compressed"] = df["string"].apply(compress_string)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["aabcccccaaa", "abcdef", "aabb", "aaabbc"],
                    "compressed": ["a2b1c5a3", "abcdef", "aabb", "aaabbc"]
                }),
                "big_o_explanation": "Time Complexity: O(N) primarily executing the loop iteration framework. Checking length `len(compressed_str)` relies on pre-tracked counts internally via Python taking only O(1) logic. Space Complexity: O(N) tracking list blocks and rendering final string comparison constraints out.",
                "follow_up_probes": [
                    "If we are comparing lengths, do we still need to process the entire string all the way to the end? (Optimization discussion)",
                    "How could you optimize the space complexity if we expect many inputs to be longer when 'compressed'?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Empty Strings and Mixed Contexts",
                "scenario": "Now we need to ensure our function is robust enough for real-world scenarios. We might receive empty strings, or strings that contain spaces and numbers alongside letters. Ensure your function gracefully handles empty strings without throwing an index error, and groups numbers/spaces correctly.",
                "hint": "Add an early return guard check for empty strings. Make sure your main counting loop relies on generic string equality so it natively supports digits and spaces too.",
                "data": pd.DataFrame({
                    "string": ["", "aabcccccaaa", "abcdef", "aaa   bb222"]
                }),
                "evaluation_criteria": [
                    "Includes a guard clause to immediately process empty string inputs and avoid an IndexError.",
                    "Proves the prior structural logic naturally accommodates numbers and space characters without specific letter validations."
                ],
                "solution_code": """\
def compress_string(s):
    if not s:
        return ""
        
    compressed = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            compressed.append(s[i - 1] + str(count))
            count = 1
            
    compressed.append(s[-1] + str(count))
    compressed_str = "".join(compressed)
    
    return compressed_str if len(compressed_str) < len(s) else s

df["compressed"] = df["string"].apply(compress_string)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["", "aabcccccaaa", "abcdef", "aaa   bb222"],
                    "compressed": ["", "a2b1c5a3", "abcdef", "a3 3b223"]
                }),
                "big_o_explanation": "Time Complexity: O(N). The guard evaluation block terminates execution completely in O(1) minimizing effort, maintaining N looping operations identically against pure standard strings vs spacing/numbers structure variables. Space Complexity: O(N) logic preserves identically against memory blocks required.",
                "follow_up_probes": [
                    "If `s` is None instead of an empty string, does your guard clause catch it safely?",
                    "How would this function need to change if we wanted it to be completely case-insensitive?"
                ]
            }
        ]
    }
