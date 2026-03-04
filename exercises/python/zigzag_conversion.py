import pandas as pd

def get_exercise():
    return {
        "title": "ZigZag Conversion",
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
        "deep_dive": "This approach simulates the ZigZag traversal directly. By keeping track of the current row and direction, we iterate through the sequence of characters exactly once. Time complexity is O(N) where N is the length of the string. Space complexity is O(N) because the result string and intermediate row array store no more than N total characters."
    }
