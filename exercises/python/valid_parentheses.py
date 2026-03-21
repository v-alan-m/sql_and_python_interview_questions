import pandas as pd

def get_exercise():
    return {
        "title": "Valid Parentheses",
        "subtitle": "Stacks, Recursion, Loops, Arrays / Lists, Hash Maps / Dictionaries",
        "description": "Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. Open brackets must be closed by the same type of brackets, and they must be closed in the correct order.",
        "data": pd.DataFrame({
            "string": ["()", "()[]{}", "(]", "([)]", "{[]}"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Use a Stack data structure (a Python list works perfectly using `.append()` and `.pop()`). When you see an opening bracket, push it to the stack. When you see a closing bracket, pop from the stack and ensure they form a matching pair.",
        "hint_sql": "Not applicable",
        "solution_python": """
def is_valid_parentheses(s):
    stack = []
    # Mapping of closing brackets to their corresponding opening brackets
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping.values():
            # If it's an opening bracket, push to stack
            stack.append(char)
        elif char in mapping.keys():
            # If it's a closing bracket
            if not stack:
                return False
            top_element = stack.pop()
            if mapping[char] != top_element:
                return False
        else:
            # Ignore non-bracket characters if any exist
            continue
            
    # Stack must be empty at the end for it to be valid
    return len(stack) == 0

df["is_valid"] = df["string"].apply(is_valid_parentheses)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "This is the classic Stack algorithmic problem. Because we process each character exactly once and stack operations (append/pop) are O(1), the time complexity is strictly linear O(N). Space complexity is O(N) in the worst case where the string is composed entirely of opening brackets e.g. '((((((', leading to all characters being pushed to the stack.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Single Bracket Type (Counter Approach)",
                "scenario": "You receive a DataFrame with a column 'string' containing strings composed only of '(' and ')'. Determine if each string has valid matching parentheses. Add a column 'is_valid' with True or False.",
                "hint": "With only one bracket type, you don't need a full stack. A simple counter that increments on '(' and decrements on ')' is sufficient. If the counter ever goes negative, the string is invalid. If it ends at zero, it's valid.",
                "data": pd.DataFrame({
                    "string": ["()", "(())", ")(", "(()"]
                }),
                "evaluation_criteria": [
                    "Can the candidate identify that a single bracket type can be solved with a counter?",
                    "Correct use of .apply() to add a new column.",
                    "Handling the 'goes negative' early-exit case — ')(' is invalid even though counts balance."
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({"string": ["()", "(())", ")(", "(()"]})

def is_valid_parentheses(s):
    count = 0
    for char in s:
        if char == '(':
            count += 1
        elif char == ')':
            count -= 1
        if count < 0:
            return False
    return count == 0

df["is_valid"] = df["string"].apply(is_valid_parentheses)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["()", "(())", ")(", "(()"],
                    "is_valid": [True, True, False, False]
                }),
                "follow_up_probes": [
                    "Why does ')(' fail even though it has equal numbers of '(' and ')'? → The closing bracket appears before any opening bracket, so count goes to -1.",
                    "What is the time and space complexity? → O(N) time, O(1) space — no stack needed.",
                    "Why is a counter sufficient here but won't work when we add more bracket types?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Mixed Bracket Types (Stack + Mapping)",
                "scenario": "Now the strings can contain three bracket types: '()', '{}', and '[]'. A simple counter won't work anymore because '([)]' has balanced counts of each type but is not valid — the nesting order matters. Update your solution to handle all three types.",
                "hint": "Use a stack (Python list). Push opening brackets. When you see a closing bracket, pop from the stack and check that it matches. A dictionary mapping closing → opening brackets keeps this clean.",
                "data": pd.DataFrame({
                    "string": ["()", "()[]{}", "(]", "([)]", "{[]}"]
                }),
                "evaluation_criteria": [
                    "Transition from counter to stack-based approach.",
                    "Using a mapping dictionary for bracket pairs.",
                    "Handling the mismatch case ('(]') and interleaving case ('([)]')."
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({"string": ["()", "()[]{}", "(]", "([)]", "{[]}"]})

def is_valid_parentheses(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            if not stack:
                return False
            if stack.pop() != mapping[char]:
                return False

    return len(stack) == 0

df["is_valid"] = df["string"].apply(is_valid_parentheses)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["()", "()[]{}", "(]", "([)]", "{[]}"],
                    "is_valid": [True, True, False, False, True]
                }),
                "follow_up_probes": [
                    "Walk through '([)]' step by step with the stack. → Push '(', push '[', see ')' → pop '[' → '[' ≠ '(' → return False.",
                    "Why is a dictionary the right data structure for the mapping? → O(1) lookup, clean code, easy to extend.",
                    "How much code changed from Stage 1? → The counter was replaced with a stack and mapping. The iteration structure stayed the same."
                ]
            },
            {
                "stage_number": 3,
                "title": "Deep Nesting, Empty Strings & Edge Cases",
                "scenario": "The data now includes edge cases: empty strings (which are considered valid), deeply nested brackets, strings with only opening brackets, strings with only closing brackets, and single-character strings. Ensure your solution handles all of these robustly without special-casing.",
                "hint": "If your stack-based solution from Stage 2 is written cleanly, it should already handle most of these edge cases naturally. An empty string means zero iterations → empty stack → valid. A single closer means the stack is empty at pop time → invalid.",
                "data": pd.DataFrame({
                    "string": ["", "{[()]}", "(((", ")))", "{[({[()]})]()}", "]"]
                }),
                "evaluation_criteria": [
                    "Empty string handling — does the code crash or return True correctly?",
                    "Deeply nested valid brackets — the stack grows and unwinds correctly.",
                    "Only-openers and only-closers — testing both failure modes.",
                    "Single closing bracket — the 'not stack' guard triggers immediately.",
                    "Code stability — zero changes needed from Stage 2 for a well-written solution."
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({"string": ["", "{[()]}", "(((", ")))", "{[({[()]})]()}", "]"]})

def is_valid_parentheses(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            if not stack:
                return False
            if stack.pop() != mapping[char]:
                return False

    return len(stack) == 0

df["is_valid"] = df["string"].apply(is_valid_parentheses)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["", "{[()]}", "(((", ")))", "{[({[()]})]()}", "]"],
                    "is_valid": [True, True, False, False, True, False]
                }),
                "follow_up_probes": [
                    "How many lines of code did you change from Stage 2? → Ideally zero. A well-designed stack solution handles all these cases inherently.",
                    "What is the worst-case space complexity? → O(N) when the entire string is opening brackets, e.g., '((((('.",
                    "Could you solve this with recursion instead of a stack? What are the trade-offs? → Yes, but recursion adds call-stack overhead and risks stack overflow on deeply nested inputs."
                ]
            },
            {
                "stage_number": 4,
                "title": "Non-Bracket Characters Interspersed",
                "scenario": "The input strings now contain non-bracket characters mixed in (e.g., letters, digits, spaces). Your solution should ignore any character that isn't one of the six bracket characters and only validate the bracket structure. This simulates validating bracket balance in real code snippets.",
                "hint": "Add a 'continue' or 'else' branch for characters that are neither openers nor closers. If your Stage 2/3 solution already uses 'elif' for closers, simply adding an 'else: continue' will skip non-bracket characters.",
                "data": pd.DataFrame({
                    "string": ["(a + b)", "func({x: [1, 2]})", "if (a > b] { go }", "123", "", "{arr[i] = (x + y)}"]
                }),
                "evaluation_criteria": [
                    "Ability to filter out irrelevant characters in a character-by-character scan.",
                    "Minimal code changes from Stage 3 — just an else: continue clause.",
                    "Robustness against strings with no brackets at all (should return True).",
                    "Mixed bracket types + non-bracket characters simultaneously."
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({"string": ["(a + b)", "func({x: [1, 2]})", "if (a > b] { go }", "123", "", "{arr[i] = (x + y)}"]})

def is_valid_parentheses(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}

    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            if not stack:
                return False
            if stack.pop() != mapping[char]:
                return False
        else:
            continue

    return len(stack) == 0

df["is_valid"] = df["string"].apply(is_valid_parentheses)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["(a + b)", "func({x: [1, 2]})", "if (a > b] { go }", "123", "", "{arr[i] = (x + y)}"],
                    "is_valid": [True, True, False, True, True, True]
                }),
                "follow_up_probes": [
                    "How much code changed from Stage 3? → Only one line: else: continue. Core logic is identical.",
                    "In a real-world linter or code formatter, what additional considerations would you need? → String literals, comments, and escaped characters should be excluded from bracket matching.",
                    "Could you solve this problem without a stack using regex? → You could use iterative regex substitution (remove innermost valid pairs until none remain), but it's O(N²) vs O(N) with a stack."
                ]
            }
        ]
    }
