import pandas as pd

def get_exercise():
    return {
        "title": "Isomorphic Strings",
        "description": "Given two strings `s` and `t`, determine if they are isomorphic. Two strings are isomorphic if the characters in `s` can be replaced to get `t`. All occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character.",
        "data": pd.DataFrame({
            "s": ["egg", "foo", "paper", "ab"],
            "t": ["add", "bar", "title", "aa"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Maintain two dictionaries (or one dictionary and one set): one to map chars from `s` to `t`, and another to keep track of chars in `t` that have already been mapped to prevent two different characters in `s` from mapping to the same character in `t`.",
        "hint_sql": "Not applicable",
        "solution_python": """
def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
        
    s_to_t_mapping = {}
    mapped_t_values = set()
    
    for char_s, char_t in zip(s, t):
        if char_s in s_to_t_mapping:
            # Check if existing mapping matches the current t char
            if s_to_t_mapping[char_s] != char_t:
                return False
        else:
            # Check if the t char has already been mapped to by a different s char
            if char_t in mapped_t_values:
                return False
            
            # Create a new mapping
            s_to_t_mapping[char_s] = char_t
            mapped_t_values.add(char_t)
            
    return True

df["isomorphic"] = df.apply(lambda row: is_isomorphic(row["s"], row["t"]), axis=1)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "This algorithm uses dual-tracking to ensure a true bi-directional (1-to-1) mapping. Iterating characters simultaneously via `zip()` is O(N) where N is string length. Dictionary checks and insertions are amortized O(1). Thus, the time complexity is linear O(N). Space complexity is O(C) where C is the size of the character set (e.g., 26 for lowercase alphabet), making it effectively O(1)."
    }
