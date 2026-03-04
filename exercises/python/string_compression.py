import pandas as pd

def get_exercise():
    return {
        "title": "String Compression",
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
        "deep_dive": "String concatenation in Python creates a new string each time, which can take O(N^2) time if done repeatedly. By appending to a list and then using `''.join()`, the algorithm runs in O(N) time complexity where N is the length of the string. The space complexity is also O(N) to store the compressed representation."
    }
