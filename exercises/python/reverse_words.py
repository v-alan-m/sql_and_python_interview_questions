import pandas as pd

def get_exercise():
    return {
        "title": "Reverse Words",
        "subtitle": "Loops, Arrays / Lists",
        "description": "Given a column of sentences, reverse the order of the words in each sentence while keeping the words themselves intact. Multiple spaces should be reduced to a single space.",
        "data": pd.DataFrame({
            "sentence": [
                "Hello world", 
                "  Python   is awesome  ", 
                "Data Engineering prep"
            ]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Use the `.split()` method (with no arguments, it handles multiple spaces automatically) to break the sentence into a list of words. Reverse that list, and then join it back together with spaces.",
        "hint_sql": "Not applicable",
        "solution_python": """
def reverse_sentence(sentence):
    # split() without arguments handles multiple whitespaces automatically
    words = str(sentence).split()
    # Reverse the list of words and join with a single space
    return " ".join(words[::-1])

df["reversed"] = df["sentence"].apply(reverse_sentence)
result = df
""",
        "solution_sql": "Not applicable",
        "big_o_explanation": "Time Complexity: O(N) where N is the length of the string, as `split()` and `join()` both iterate through the entire string once. Space Complexity: O(N) primarily because we must allocate memory for the intermediate list of words and the newly constructed string.",
        "deep_dive": "String splitting and joining in Python happens in O(N) time complexity, where N is the length of the string. The list reversal `words[::-1]` also operates in O(K) where K is the number of words. The space complexity is O(N) to store the intermediate list of words and the new string.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Reversal",
                "scenario": "Let's start simple. We have a column of strings where each string contains words separated by exactly one space. I'd like you to reverse the order of the words in each string.",
                "hint": "You can use the `.split(\" \")` method to turn the sentence into a list of words, reverse that list, and then join it back together.",
                "data": pd.DataFrame({
                    "sentence": [
                        "Hello world",
                        "Data Engineering prep",
                        "cats and dogs"
                    ]
                }),
                "evaluation_criteria": [
                    "Basic familiarity with string manipulation methods (`split`, `join`).",
                    "Knowledge of list reversal in Python (`[::-1]` or `reversed()`).",
                    "Using pandas `.apply()` or a lambda function to apply row-wise transformations."
                ],
                "solution_code": """\
def reverse_sentence(sentence):
    # Split by exact space since we assume clean data for now
    words = sentence.split(" ")
    return " ".join(words[::-1])

df["reversed"] = df["sentence"].apply(reverse_sentence)
result = df
""",
                "expected_output": pd.DataFrame({
                    "sentence": [
                        "Hello world",
                        "Data Engineering prep",
                        "cats and dogs"
                    ],
                    "reversed": [
                        "world Hello",
                        "prep Engineering Data",
                        "dogs and cats"
                    ]
                }),
                "big_o_explanation": "Time Complexity: O(N) where N is the number of characters. `.split(\" \")` takes O(N) time, reversing takes O(N/M) time (where M is average word length), and `.join()` takes O(N) time. Overall it's O(N). Space Complexity: O(N) to maintain the list of substrings and the rebuilt string.",
                "follow_up_probes": [
                    "Time Complexity: What's the Big-O time complexity of your approach?",
                    "Space Complexity: How much extra memory does creating the list of words take?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Irregular Spacing",
                "scenario": "Good. Now, real-world data is rarely perfectly formatted. Some sentences have leading or trailing spaces, or multiple consecutive spaces between words. We want to reduce all those down to a single space separating the reversed words.",
                "hint": "Instead of passing `\" \"` to `.split()`, what happens if you call `.split()` without any arguments?",
                "data": pd.DataFrame({
                    "sentence": [
                        "Hello world",
                        "  Python   is awesome  ",
                        "one  two   three",
                        "Data Engineering prep"
                    ]
                }),
                "evaluation_criteria": [
                    "Awareness of default behaviors of Python built-ins.",
                    "Understanding how to handle irregular whitespace clean-up automatically instead of writing complex regex checks."
                ],
                "solution_code": """\
def reverse_sentence(sentence):
    # split() without arguments handles arbitrary amounts of whitespace
    # and strips leading/trailing spaces automatically
    words = sentence.split()
    return " ".join(words[::-1])

df["reversed"] = df["sentence"].apply(reverse_sentence)
result = df
""",
                "expected_output": pd.DataFrame({
                    "sentence": [
                        "Hello world",
                        "  Python   is awesome  ",
                        "one  two   three",
                        "Data Engineering prep"
                    ],
                    "reversed": [
                        "world Hello",
                        "awesome is Python",
                        "three two one",
                        "prep Engineering Data"
                    ]
                }),
                "big_o_explanation": "Time Complexity: O(N). The `.split()` method internally trims trailing/leading spaces and handles multiple spaces, but it still parses the string in a single O(N) pass, effectively matching our prior solution's time complexity. Space Complexity: O(N) because the size of the intermediate array is still proportional to the number of words generated.",
                "follow_up_probes": [
                    "Regex Alternative: If `.split()` didn't have this behavior built-in, how would you approach this using the `re` module?",
                    "Trailing Spaces: Does your current logic leave trailing spaces at the start or end of the reversed string?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Type Safety & Edge Cases",
                "scenario": "Excellent. Finally, our data engineers noticed our pipeline occasionally crashes because some rows contain pure whitespace, empty strings, or even non-string numerical data. Let's make your function robust against these edge cases without failing.",
                "hint": "Ensure you explicitly convert the input to a string before treating it like one. Think about how `split()` handles empty or pure whitespace strings.",
                "data": pd.DataFrame({
                    "sentence": [
                        "Hello world",
                        "  Python   is awesome  ",
                        "Word",
                        "",
                        "   ",
                        12345
                    ]
                }),
                "evaluation_criteria": [
                    "Defensive programming.",
                    "Type coercion (`str()`).",
                    "Understanding that `.split()` on empty or whitespace strings evaluates safely to an empty list `[]`, and `' '.join([])` yields `\"\"`."
                ],
                "solution_code": """\
def reverse_sentence(sentence):
    # Cast to string to handle numeric types or None objects gracefully
    # split() handles the empty string/whitespace scenarios cleanly
    words = str(sentence).split()
    return " ".join(words[::-1])

df["reversed"] = df["sentence"].apply(reverse_sentence)
result = df
""",
                "expected_output": pd.DataFrame({
                    "sentence": [
                        "Hello world",
                        "  Python   is awesome  ",
                        "Word",
                        "",
                        "   ",
                        12345
                    ],
                    "reversed": [
                        "world Hello",
                        "awesome is Python",
                        "Word",
                        "",
                        "",
                        "12345"
                    ]
                }),
                "big_o_explanation": "Time Complexity: O(N). Converting primitive values using `str()` takes linear time proportional to the value's length. The remainder of the string parsing `split` and `join` maintains O(N) time complexity. Space Complexity: O(N) to handle the new typed intermediate string representations alongside the arrays.",
                "follow_up_probes": [
                    "Null Handling: Your solution casts to string, making `None` become `\"None\"`. Is there a scenario where you'd prefer to return `None` or an empty string instead? How would you implement that check?",
                    "In-place Reversal Challenge: In a lower-level language like C or C++, how would you perform this reversal in-place without allocating O(N) memory? (Hint: Reverse the entire string, then reverse each individual word)."
                ]
            }
        ]
    }
