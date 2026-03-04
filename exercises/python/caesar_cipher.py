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
        "solution_python": """
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
        "deep_dive": "This string mutation algorithm requires looking at every character in the string once, resulting in an O(N) time complexity where N is the length of the string. Space complexity is O(N) due to the use of a list to build up the mutated string before joining it, which avoids the O(N^2) trap of immutable string concatenations inside a loop."
    }
