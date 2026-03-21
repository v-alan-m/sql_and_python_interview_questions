import pandas as pd

def get_exercise():
    return {
        "title": "ZigZag Conversion",
        "subtitle": "Loops, Arrays / Lists",
        "description": "The string 'PAYPALISHIRING' is written in a zigzag pattern on a given number of rows like this:\nP   A   H   N\nA P L S I I G\nY   I   R\nAnd then read line by line: 'PAHNAPLSIIGYIR'. Write the code that takes a string and makes this conversion given a number of rows.",
        "data": pd.DataFrame({
            "string": ["PAYPALISHIRING", "PAYPALISHIRING", "A"],
            "num_rows": [3, 4, 1]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Create an array of strings (or lists) to represent each row. Iterate through the string, appending characters to the current row. Use a boolean flag to track whether you are moving 'down' or 'up' the zigzag, changing direction when you hit the top or bottom row.",
        "hint_sql": "Not applicable",
        "solution_python": """
def convert_zigzag(s, numRows):
    if numRows == 1 or numRows >= len(s):
        return s
        
    # Initialize a list of strings for each row
    rows = ["" for _ in range(min(numRows, len(s)))]
    current_row = 0
    going_down = False
    
    for char in s:
        rows[current_row] += char
        
        # Change direction at boundaries
        if current_row == 0 or current_row == numRows - 1:
            going_down = not going_down
            
        current_row += 1 if going_down else -1
        
    return "".join(rows)

df["zigzag_result"] = df.apply(lambda row: convert_zigzag(row["string"], row["num_rows"]), axis=1)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "This approach simulates the ZigZag traversal directly. By keeping track of the current row and direction, we iterate through the sequence of characters exactly once. Time complexity is O(N) where N is the length of the string. Space complexity is O(N) because the result string and intermediate row array store no more than N total characters.",
        "big_o_explanation": "### ⏱️ Optimal Big O Notation\n**Time Complexity:** `O(N)` where N is the length of the string. We look at every character exactly one time.\n**Space Complexity:** `O(N)`. We build a string (or array of rows) that stores exactly N characters. The array containing the rows is limited to `min(numRows, N)` which scales at worst case exactly to `O(N)`.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Two-Row Alternation",
                "scenario": "To start, let's write a function that takes a string and distributes its characters alternately between two rows (like dealing cards into two hands), then combines them into a single string. Assume `numRows` is always exactly 2 for now.",
                "hint": "Create two string variables or a list of two empty strings. Iterate through the input string, appending characters to the first row, then the second row, then back to the first. You can use a toggle variable or `index % 2`.",
                "data": pd.DataFrame({
                    "string": ["HELLO", "WORLD", "PYTHON"],
                    "num_rows": [2, 2, 2]
                }),
                "evaluation_criteria": [
                    "Basic String iteration and string building",
                    "State toggling or modulo arithmetic"
                ],
                "solution_code": """\
def process_stage(s):
    rows = ["", ""]
    current = 0
    for char in s:
        rows[current] += char
        current = 1 - current
    return "".join(rows)

df["zigzag_result"] = df.apply(lambda row: process_stage(row["string"]), axis=1)
result = df""",
                "expected_output": pd.DataFrame({
                    "string": ["HELLO", "WORLD", "PYTHON"],
                    "num_rows": [2, 2, 2],
                    "zigzag_result": ["HLOEL", "WRDOL", "PTOYHN"]
                }),
                "follow_up_probes": [
                    "What is the time and space complexity of your approach?",
                    "Can you write this using python slice notation `s[::2] + s[1::2]` instead of a loop?"
                ],
                "big_o_explanation": "#### Stage 1: Two-Row Alternation\n**Time Complexity:** `O(N)`. We iterate through the string once, performing constant `O(1)` string concatenation steps.\n**Space Complexity:** `O(N)`. We create two separate string buffers whose combined lengths equal the original string `N`."
            },
            {
                "stage_number": 2,
                "title": "Full ZigZag Pattern",
                "scenario": "Now let's generalize this. Instead of strictly alternating between two rows, the characters should move down the rows until they hit `numRows`, then move diagonally up until they hit the first row, repeating this zigzag pattern.",
                "hint": "You'll need an array of strings `rows` of size `num_rows`. Keep track of the `current_row` and a boolean `going_down`. When you hit the top (0) or bottom (`numRows - 1`), reverse the direction.",
                "data": pd.DataFrame({
                    "string": ["PAYPALISHIRING", "PAYPALISHIRING", "PYTHON"],
                    "num_rows": [3, 4, 2]
                }),
                "evaluation_criteria": [
                    "Advanced state tracking (direction flag)",
                    "Boundary detection within an array",
                    "Extensibility of the previous logic"
                ],
                "solution_code": """\
def process_stage(s, numRows):
    rows = ["" for _ in range(numRows)]
    current_row = 0
    going_down = False
    
    for char in s:
        rows[current_row] += char
        if current_row == 0 or current_row == numRows - 1:
            going_down = not going_down
        current_row += 1 if going_down else -1
        
    return "".join(rows)

df["zigzag_result"] = df.apply(lambda row: process_stage(row["string"], row["num_rows"]), axis=1)
result = df""",
                "expected_output": pd.DataFrame({
                    "string": ["PAYPALISHIRING", "PAYPALISHIRING", "PYTHON"],
                    "num_rows": [3, 4, 2],
                    "zigzag_result": ["PAHNAPLSIIGYIR", "PINALSIGYAHRPI", "PTOYHN"]
                }),
                "follow_up_probes": [
                    "Why is creating an array of strings better than evaluating the math behind the string indices?",
                    "What bug might happen if `numRows` is 1? Walk through your loop logic."
                ],
                "big_o_explanation": "#### Stage 2: Full ZigZag Pattern\n**Time Complexity:** `O(N)`. Still a single pass through the sequence of characters.\n**Space Complexity:** `O(N)`. We create an array of `numRows` elements, but collectively they only store `N` characters."
            },
            {
                "stage_number": 3,
                "title": "Handling Edge Cases",
                "scenario": "Your code works great for standard zigzag patterns, but what if `numRows` is 1? Or what if the input string is shorter than `numRows`? Update your logic to handle these edge cases robustly.",
                "hint": "If `numRows` is 1, the `current_row` becomes 0, and the direction changes back and forth, but it will try to increment/decrement out of bounds or get stuck. Add a guard clause early or prevent out of bounds when allocating `rows` array.",
                "data": pd.DataFrame({
                    "string": ["A", "AB", "PAYPALISHIRING", "X", "SHORT"],
                    "num_rows": [1, 1, 3, 5, 10]
                }),
                "evaluation_criteria": [
                    "Edge case identification and handling",
                    "Short-circuit early returns",
                    "Array memory optimization"
                ],
                "solution_code": """\
def process_stage(s, numRows):
    if numRows == 1 or numRows >= len(s):
        return s
        
    rows = ["" for _ in range(min(numRows, len(s)))]
    current_row = 0
    going_down = False
    
    for char in s:
        rows[current_row] += char
        if current_row == 0 or current_row == numRows - 1:
            going_down = not going_down
        current_row += 1 if going_down else -1
        
    return "".join(rows)

df["zigzag_result"] = df.apply(lambda row: process_stage(row["string"], row["num_rows"]), axis=1)
result = df""",
                "expected_output": pd.DataFrame({
                    "string": ["A", "AB", "PAYPALISHIRING", "X", "SHORT"],
                    "num_rows": [1, 1, 3, 5, 10],
                    "zigzag_result": ["A", "AB", "PAHNAPLSIIGYIR", "X", "SHORT"]
                }),
                "follow_up_probes": [
                    "Why do we check `numRows >= len(s)` in the guard clause? What does it save us?",
                    "What is the final space and time complexity for the optimal solution?"
                ],
                "big_o_explanation": "#### Stage 3: Handling Edge Cases\n**Time Complexity:** `O(N)`. If a case gets caught early by the guard clause, it bypasses computation but does not fundamentally alter the worst-case `N` loop.\n**Space Complexity:** `O(N)`. The guard clauses efficiently prevent out of bounds memory allocation errors."
            }
        ]
    }
