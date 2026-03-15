import pandas as pd

def get_exercise():
    return {
        "title": "Caesar Cipher",
        "description": "Implement a Caesar cipher that shifts every alphabet character in a string by a given integer offset. The shift should wrap around the alphabet (e.g., shifting 'z' by 1 gives 'a'). Preserve the case of the characters and leave non-alphabet characters unchanged.",
        "data": pd.DataFrame({
            "string": ["Hello, World!", "abc", "XYZ", "Python 3!"],
            "shift_amount": [3, 1, 5, -2]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Iterate through the string. Use the `ord()` function to get the numeric ASCII value of a character and `chr()` to convert back. Use modulo `% 26` to handle wrapping around the alphabet.",
        "hint_sql": "Not applicable",
        "solution_python": """\
def caesar_cipher(text, shift):
    result = []
    
    for char in text:
        if char.isalpha():
            # Determine base ASCII value based on case
            base = ord('a') if char.islower() else ord('A')
            
            # Apply shift, wrap with modulo, and convert back
            shifted_ord = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted_ord))
        else:
            # Leave non-alphabetic chars as is
            result.append(char)
            
    return "".join(result)

df["ciphered"] = df.apply(lambda row: caesar_cipher(row["string"], row["shift_amount"]), axis=1)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "This string mutation algorithm requires looking at every character in the string once, resulting in an O(N) time complexity where N is the length of the string. Space complexity is O(N) due to the use of a list to build up the mutated string before joining it, which avoids the O(N^2) trap of immutable string concatenations inside a loop.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Lowercase Shift (No Wrapping)",
                "scenario": "Let's implement a simplified Caesar cipher. Write a function that takes a lowercase string and shifts each character forward in the alphabet by a given integer offset. For this first step, assume the string only contains lowercase English letters, and the shift will never push a character past 'z'.",
                "hint": "You can iterate through the characters of the string. The built-in functions `ord()` will get the numeric ASCII value of a character, and `chr()` will convert an integer value back to a character.",
                "data": pd.DataFrame({
                    "string": ["abc", "hello"],
                    "shift_amount": [1, 3]
                }),
                "evaluation_criteria": [
                    "Basic string iteration.",
                    "Understanding and manipulating ASCII values using `ord()` and `chr()`.",
                    "Building a new string efficiently."
                ],
                "solution_code": """\
def caesar_cipher(text, shift):
    result = []
    for char in text:
        shifted_ord = ord(char) + shift
        result.append(chr(shifted_ord))
    return "".join(result)

df["ciphered"] = df.apply(lambda row: caesar_cipher(row["string"], row["shift_amount"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["abc", "hello"],
                    "shift_amount": [1, 3],
                    "ciphered": ["bcd", "khoor"]
                }),
                "follow_up_probes": [
                    "Why did you use a list `[]` and `\"\".join()` rather than concatenating strings with `+=`? (Strings are immutable, concatenation in a loop is O(N^2) in worst case, while lists are O(N))."
                ]
            },
            {
                "stage_number": 2,
                "title": "Alphabet Wrapping",
                "scenario": "Excellent. Now, suppose the shift _can_ push a character past 'z'. For instance, shifting 'z' by 1 should result in 'a', wrapping around the alphabet. Update your function to handle wrapping while still assuming everything is lowercase.",
                "hint": "To wrap properly, you need to normalise the ASCII value so 'a' is 0, 'b' is 1... up to 25. Then you can use the modulo operator `% 26` to wrap around, before converting back to the actual ASCII range.",
                "data": pd.DataFrame({
                    "string": ["abc", "xyz", "zebra", "python"],
                    "shift_amount": [1, 1, 2, 5]
                }),
                "evaluation_criteria": [
                    "Using modulo arithmetic for cyclic shifts.",
                    "Mathematical normalisation (subtracting the base ASCII value before modulo, then adding it back).",
                    "Still handles non-wrapping shifts correctly."
                ],
                "solution_code": """\
def caesar_cipher(text, shift):
    result = []
    for char in text:
        shifted_ord = (ord(char) - ord('a') + shift) % 26 + ord('a')
        result.append(chr(shifted_ord))
    return "".join(result)

df["ciphered"] = df.apply(lambda row: caesar_cipher(row["string"], row["shift_amount"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["abc", "xyz", "zebra", "python"],
                    "shift_amount": [1, 1, 2, 5],
                    "ciphered": ["bcd", "yza", "bgdtc", "udymts"]
                }),
                "follow_up_probes": [
                    "Will the modulo `% 26` still work effectively if `shift` is a massive number like 1000? (Yes, modulo handles extremely large rotations seamlessly)."
                ]
            },
            {
                "stage_number": 3,
                "title": "Mixed Case Support",
                "scenario": "That handles the full lowercase alphabet. In reality, text has proper nouns and capitals. Upgrade your function so it correctly preserves casing: uppercase letters remain uppercase, and lowercase remain lowercase.",
                "hint": "You'll need an `if` condition to determine the base offset (`ord('a')` vs `ord('A')`) depending on whether the current character is uppercase or lowercase.",
                "data": pd.DataFrame({
                    "string": ["abc", "xyz", "Xyz", "ZeBra", "Python"],
                    "shift_amount": [1, 1, 1, 2, 5]
                }),
                "evaluation_criteria": [
                    "Conditional logic based on character properties (`.islower()` or `.isupper()`).",
                    "Generalising the modulo algorithm to dynamic bases.",
                    "Still handles plain lowercase and wrapping correctly."
                ],
                "solution_code": """\
def caesar_cipher(text, shift):
    result = []
    for char in text:
        base = ord('a') if char.islower() else ord('A')
        shifted_ord = (ord(char) - base + shift) % 26 + base
        result.append(chr(shifted_ord))
    return "".join(result)

df["ciphered"] = df.apply(lambda row: caesar_cipher(row["string"], row["shift_amount"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["abc", "xyz", "Xyz", "ZeBra", "Python"],
                    "shift_amount": [1, 1, 1, 2, 5],
                    "ciphered": ["bcd", "yza", "Yza", "BgDtc", "Udymts"]
                }),
                "follow_up_probes": [
                    "If this function processes millions of characters and the casing is completely randomized, what impact might `if char.islower()` have on performance at a low level?"
                ]
            },
            {
                "stage_number": 4,
                "title": "Non-Alphabetic Characters & Negative Shifts",
                "scenario": "For the final version, strings will also contain spaces, punctuation, and numbers. Your function should leave any non-alphabet character untouched. Additionally, what happens if the shift is negative (e.g., decrypting)? Make sure your algorithm is robust for negative shifts too.",
                "hint": "Use `.isalpha()` to check whether to shift a character or append it as-is. In Python, the `%` operator elegantly correctly handles negative numbers (e.g., `-1 % 26` is `25`), so your math shouldn't need changing!",
                "data": pd.DataFrame({
                    "string": ["abc", "Xyz", "Hello, World!", "Python 3.9", "Yza"],
                    "shift_amount": [1, 1, 3, 5, -1]
                }),
                "evaluation_criteria": [
                    "Handling edge cases safely (`.isalpha()`).",
                    "Recognition of negative modulo behaviour in Python.",
                    "Still handles plain lowercase, mixed case, and wrapping correctly."
                ],
                "solution_code": """\
def caesar_cipher(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            shifted_ord = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted_ord))
        else:
            result.append(char)
    return "".join(result)

df["ciphered"] = df.apply(lambda row: caesar_cipher(row["string"], row["shift_amount"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["abc", "Xyz", "Hello, World!", "Python 3.9", "Yza"],
                    "shift_amount": [1, 1, 3, 5, -1],
                    "ciphered": ["bcd", "Yza", "Khoor, Zruog!", "Udymts 3.9", "Xyz"]
                }),
                "follow_up_probes": [
                    "In Python, `-2 % 26 = 24`. In languages like C++ or Java, it might evaluate to `-2` unless handled. How would you handle negative wrap-around if your language didn't smoothly perform modulo on negatives? (Add 26 before the modulo)."
                ]
            }
        ]
    }
