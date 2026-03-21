import pandas as pd

def get_exercise():
    return {
        "title": "Isomorphic Strings",
        "subtitle": "Loops, Hash Maps / Dictionaries, Sets",
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
        "deep_dive": "This algorithm uses dual-tracking to ensure a true bi-directional (1-to-1) mapping. Iterating characters simultaneously via `zip()` is O(N) where N is string length. Dictionary checks and insertions are amortized O(1). Thus, the time complexity is linear O(N). Space complexity is O(C) where C is the size of the character set (e.g., 26 for lowercase alphabet), making it effectively O(1).",
        "big_o_explanation": "This algorithm simultaneously tracks characters using a dictionary and a set. Iterating simultaneously via `zip()` is exactly `O(N)` Time. The dictionary inserts and set validations are amortized `O(1)`. Overall Time Complexity is **O(N)**. Space Complexity is bounded by the size of the alphabet `O(C)` which is constant, meaning it is effectively **O(1)** memory footprint.",
        
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Unidirectional Mapping",
                "scenario": "Given two strings `s` and `t`, check if the characters in `s` can be replaced to get `t`. In this basic version, multiple characters in `s` *can* map to the same character in `t` (we only care that `s` characters consistently map to the *same* `t` character).",
                "hint": "You can iterate through both strings simultaneously and use a single dictionary map corresponding characters from `s` to `t`. If you see an `s` character again, check if it maps to the same `t` character as before.",
                "data": pd.DataFrame({"s": ["egg", "foo", "paper", "ab", "python script"], "t": ["add", "bar", "title", "aa", "python script"]}),
                "evaluation_criteria": [
                    "Uses `zip` or index iteration correctly to process characters in parallel",
                    "Uses a dictionary to store the mapping from `s` to `t`",
                    "Correctly returns `False` when an existing `s` character maps to a new, different `t` character"
                ],
                "solution_code": """\\
def is_isomorphic_stage_1(s, t):
    if len(s) != len(t):
        return False
        
    s_to_t = {}
    
    for char_s, char_t in zip(s, t):
        if char_s in s_to_t:
            if s_to_t[char_s] != char_t:
                return False
        else:
            s_to_t[char_s] = char_t
            
    return True

df["isomorphic"] = df.apply(lambda row: is_isomorphic_stage_1(row["s"], row["t"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "s": ["egg", "foo", "paper", "ab", "python script"],
                    "t": ["add", "bar", "title", "aa", "python script"],
                    "isomorphic": [True, False, True, True, True]
                }),
                "follow_up_probes": [
                    "Why does `ab` -> `aa` return `True` here?",
                    "If the strings can be different lengths, what should the function return immediately?"
                ],
                "big_o_explanation": "In Python, `zip(s, t)` streams characters linearly without building huge arrays. Evaluating each pair takes `O(1)` Time via the dictionary. Thus, the loop finishes in **O(N) Time**. The dictionary tracks at most 256 unique ASCII characters, keeping Space strictly bounded inside **O(1)** Space."
            },
            {
                "stage_number": 2,
                "title": "True Bi-Directional Mapping",
                "scenario": "Now let's apply the strict definition of isomorphic strings: **No two characters may map to the same character.** This means the mapping must be 1-to-1 (bi-directional).",
                "hint": "You need to ensure that the `t` character hasn't already been mapped to by a *different* `s` character. A second dictionary or a set can help track already mapped `t` values.",
                "data": pd.DataFrame({"s": ["egg", "foo", "paper", "ab", "badc", "hot dog"], "t": ["add", "bar", "title", "aa", "baba", "bat man"]}),
                "evaluation_criteria": [
                    "Prevents multiple different `s` characters from mapping to the same `t` character",
                    "Uses a set or second dictionary to track `t` characters",
                    "Successfully handles cases where length matches but character uniqueness fails (like `ab` -> `aa`)"
                ],
                "solution_code": """\\
def is_isomorphic_stage_2(s, t):
    if len(s) != len(t):
        return False
        
    s_to_t = {}
    mapped_t = set()
    
    for char_s, char_t in zip(s, t):
        if char_s in s_to_t:
            if s_to_t[char_s] != char_t:
                return False
        else:
            if char_t in mapped_t:
                return False
            s_to_t[char_s] = char_t
            mapped_t.add(char_t)
            
    return True

df["isomorphic"] = df.apply(lambda row: is_isomorphic_stage_2(row["s"], row["t"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "s": ["egg", "foo", "paper", "ab", "badc", "hot dog"],
                    "t": ["add", "bar", "title", "aa", "baba", "bat man"],
                    "isomorphic": [True, False, True, False, False, True]
                }),
                "follow_up_probes": [
                    "What is the time and space complexity of adding the set?",
                    "If we know the alphabet is limited to ASCII (256 characters), how does that impact the theoretical space complexity?"
                ],
                "big_o_explanation": "Checking inclusion dynamically in a Python `set()` is incredibly fast natively, executing in `O(1)` amortized time via hashing formulas. Thus, securing a strict bi-directional restriction preserves our highly optimal **O(N) Time Complexity** and constant **O(1) Space Complexity** bounds."
            },
            {
                "stage_number": 3,
                "title": "Case Sensitivity and Whitespace Ignorance",
                "scenario": "The input data is now messy. Strings contain spaces which should NOT be considered as meaningful characters for the isomorphism check (i.e. we only care about the structural mapping of the visible characters). Also, mapping should be **case-insensitive** (so 'A' mapping to 'b' means 'a' also maps to 'b').",
                "hint": "You need to clean or normalize both strings by removing spaces and converting to lowercase before doing the mapping comparison.",
                "data": pd.DataFrame({"s": ["E g g", "f o o", "a b", "Data base", "Py thon"], "t": ["a d d", "B a r", "A A", "Code base", "Cy thon"]}),
                "evaluation_criteria": [
                    "Uses string methods (`.replace()`, `.lower()`) reliably to clean the input entirely before evaluating",
                    "Understands how to separate the data cleaning phase from the core algorithmic logic"
                ],
                "solution_code": """\\
def is_isomorphic_stage_3(s, t):
    # Data cleaning: remove spaces and normalize case
    clean_s = s.replace(" ", "").lower()
    clean_t = t.replace(" ", "").lower()
    
    if len(clean_s) != len(clean_t):
        return False
        
    s_to_t = {}
    mapped_t = set()
    
    for char_s, char_t in zip(clean_s, clean_t):
        if char_s in s_to_t:
            if s_to_t[char_s] != char_t:
                return False
        else:
            if char_t in mapped_t:
                return False
            s_to_t[char_s] = char_t
            mapped_t.add(char_t)
            
    return True

df["isomorphic"] = df.apply(lambda row: is_isomorphic_stage_3(row["s"], row["t"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "s": ["E g g", "f o o", "a b", "Data base", "Py thon"],
                    "t": ["a d d", "B a r", "A A", "Code base", "Cy thon"],
                    "isomorphic": [True, False, False, False, True]
                }),
                "follow_up_probes": [
                    "`s.replace(\" \", \"\")` creates a new string in memory. If the strings were 10GB text files, why would this data cleaning approach be problematic?",
                    "How could you achieve the space-ignoring behavior using pointers/indexes without creating a new string?"
                ],
                "big_o_explanation": "String methods like `.replace()` and `.lower()` return brand new copies of the entire string in memory. This bumps the memory utilization overhead entirely linearly to correspond with the size of N, generating an **O(N) Space Complexity**. Iterating over the new strings takes **O(N) Time**."
            },
            {
                "stage_number": 4,
                "title": "Multi-Word Preservation (Advanced Isomorphism)",
                "scenario": "Instead of removing spaces, spaces are now treated as strict word boundaries. For two strings to be isomorphic, they must have the **exact same pattern of spaces**. Furthermore, characters are mapped exactly as before, but a space character (` `) can **only** map to another space character (` `).",
                "hint": "Instead of pre-cleaning the string, iterate through the raw uncleaned strings (lowercased). Add an explicit check ensuring spaces only map to spaces.",
                "data": pd.DataFrame({"s": ["a b c", "ab c", "a b c", "foo bar", "egg foo"], "t": ["x y z", "x yz", "x yz", "baz quz", "add baz"]}),
                "evaluation_criteria": [
                    "Modifies core matching logic to treat space as a strictly reserved character",
                    "Handles structural mismatches (spaces in different positions)",
                    "Maintains bi-directional mapping logic for the rest of the alphabet"
                ],
                "solution_code": """\\
def is_isomorphic_stage_4(s, t):
    clean_s = s.lower()
    clean_t = t.lower()
    
    if len(clean_s) != len(clean_t):
        return False
        
    s_to_t = {}
    mapped_t = set()
    
    for char_s, char_t in zip(clean_s, clean_t):
        # Strict whitespace rule: space must map to space
        if (char_s == " " and char_t != " ") or (char_t == " " and char_s != " "):
            return False
            
        if char_s in s_to_t:
            if s_to_t[char_s] != char_t:
                return False
        else:
            if char_t in mapped_t:
                return False
            s_to_t[char_s] = char_t
            mapped_t.add(char_t)
            
    return True

df["isomorphic"] = df.apply(lambda row: is_isomorphic_stage_4(row["s"], row["t"]), axis=1)
result = df
""",
                "expected_output": pd.DataFrame({
                    "s": ["a b c", "ab c", "a b c", "foo bar", "egg foo"],
                    "t": ["x y z", "x yz", "x yz", "baz quz", "add baz"],
                    "isomorphic": [True, False, False, False, False]
                }),
                "follow_up_probes": [
                    "How does your algorithm handle two strings identical in length but with different space counts? Ex: `ab c` and `x yz`.",
                    "Where might this 'structural isomorphism' check be used in real-world data engineering? (e.g. validating masking/tokenisation rules on PII data)"
                ],
                "big_o_explanation": "Rather than eagerly mutating large datasets entirely, doing targeted conditional bypassing is a highly effective optimization technique. By handling exact matching rules on space literals mathematically natively, we protect our **O(N) Time Complexity** boundary with surgical accuracy, although `.lower()` itself does require **O(N) Aux Space** here unless managed with pointer offsets on exact ASCII values."
            }
        ]
    }
