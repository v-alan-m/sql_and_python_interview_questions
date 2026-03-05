import pandas as pd

def get_exercise():
    return {
        "title": "Word Frequency",
        "description": "Write a query or script to calculate the frequency of each word in a given text body. Assume the text is a single string where words are separated by spaces. Return the result sorted by frequency descending.",
        "data": pd.DataFrame({
            "text": ["the sunny day is sunny and the day is good"]
        }),
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "Extract the single string, split it into a list of words, use `collections.Counter` to get the frequencies, and convert the result back to a DataFrame.",
        "hint_sql": "SQL isn't designed for splitting strings natively into rows. You would typically need a string-splitting function (like `STRING_SPLIT` in T-SQL or `unnest(string_to_array())` in Postgres) to turn the space-separated string into rows before grouping.",
        "solution_python": """
from collections import Counter

# Extract the single string from the dataframe
text = df["text"].iloc[0]

# Split into words and count
word_counts = Counter(text.split())

# Convert to DataFrame
result = pd.DataFrame(word_counts.items(), columns=["word", "frequency"])

# Sort by frequency descending
result = result.sort_values(by="frequency", ascending=False).reset_index(drop=True)
""",
        "solution_sql": """
-- Assuming PostgreSQL syntax for string splitting into rows
WITH SplitWords AS (
    SELECT unnest(string_split(text, ' ')) AS word
    FROM table_name
)
SELECT 
    word,
    COUNT(*) as frequency
FROM SplitWords
GROUP BY word
ORDER BY frequency DESC;
""",
        "deep_dive": "Python is exceptionally well-suited for taking unstructured text and structuring it (splitting and counting). The `Counter` object makes this an O(N) operation where N is the number of characters/words. Relational databases require pivoting columns into rows (un-nesting) before they can perform their highly optimized `GROUP BY` aggregations."
    }
