import pandas as pd

def get_exercise():
    return {
        "title": "Word Frequency",
        "subtitle": "GROUP BY, Common Table Expressions (CTEs), Pandas Aggregation",
        "description": "Write a query or script to calculate the frequency of each word in a given text body. Assume the text is a single string where words are separated by spaces. Return the result sorted by frequency descending.",
        "data": pd.DataFrame({
            "text": ["the sunny day is sunny and the day is good"]
        }),
        "table_name": "documents",
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
    FROM documents
)
SELECT 
    word,
    COUNT(*) as frequency
FROM SplitWords
GROUP BY word
ORDER BY frequency DESC;
""",
        "deep_dive": "Python is exceptionally well-suited for taking unstructured text and structuring it (splitting and counting). The `Counter` object makes this an O(N) operation where N is the number of characters/words. Relational databases require pivoting columns into rows (un-nesting) before they can perform their highly optimized `GROUP BY` aggregations.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Word Frequency",
                "scenario": "Calculate the frequency of each word in a single string, returning the result sorted by frequency descending, then alphabetically.",
                "hint": "Python: split the string and use `collections.Counter`. SQL: Use `unnest(string_split(text, ' '))`.",
                "data": pd.DataFrame({
                    "text": ["apple banana apple"]
                }),
                "evaluation_criteria": [
                    "Ability to split strings into words",
                    "Familiarity with counting occurrences (e.g., Counter in Python, GROUP BY in SQL)",
                    "Basic sorting implementation"
                ],
                "solution_code": """\
from collections import Counter
import pandas as pd

text = df["text"].iloc[0]
word_counts = Counter(text.split())

result = pd.DataFrame(word_counts.items(), columns=["word", "frequency"])
result = result.sort_values(by=["frequency", "word"], ascending=[False, True]).reset_index(drop=True)
""",
                "solution_sql": """\
WITH SplitWords AS (
    SELECT unnest(string_split(text, ' ')) AS word
    FROM documents
)
SELECT 
    word,
    COUNT(*) AS frequency
FROM SplitWords
GROUP BY word
ORDER BY frequency DESC, word ASC;
""",
                "expected_output": pd.DataFrame({
                    "word": ["apple", "banana"],
                    "frequency": [2, 1]
                }),
                "follow_up_probes": [
                    "What is the time complexity of your solution?",
                    "How does `Counter` work under the hood in Python?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Multiple Documents",
                "scenario": "The input now contains multiple texts across different rows. Count the word frequency across the entire dataset.",
                "hint": "Python: Join all text strings together before splitting. SQL: unnest across all rows.",
                "data": pd.DataFrame({
                    "text": ["the sunny day", "is sunny and the", "day is good"]
                }),
                "evaluation_criteria": [
                    "Ability to iterate or join strings across multiple DataFrame rows",
                    "Understanding of how SQL CTEs natively process multiple rows"
                ],
                "solution_code": """\
from collections import Counter
import pandas as pd

# Concatenate all rows
all_text = " ".join(df["text"].dropna().tolist())
word_counts = Counter(all_text.split())

result = pd.DataFrame(word_counts.items(), columns=["word", "frequency"])
result = result.sort_values(by=["frequency", "word"], ascending=[False, True]).reset_index(drop=True)
""",
                "solution_sql": """\
WITH SplitWords AS (
    SELECT unnest(string_split(text, ' ')) AS word
    FROM documents
    WHERE text IS NOT NULL
)
SELECT 
    word,
    COUNT(*) AS frequency
FROM SplitWords
GROUP BY word
ORDER BY frequency DESC, word ASC;
""",
                "expected_output": pd.DataFrame({
                    "word": ["day", "is", "sunny", "the", "and", "good"],
                    "frequency": [2, 2, 2, 2, 1, 1]
                }),
                "follow_up_probes": [
                    "If we had a billion rows, would concatenating everything in memory be a good idea?",
                    "How would you optimize the Python solution for a very large dataset?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Case-Insensitivity & Missing Data",
                "scenario": "Real-world data is messy. Treat capital and lowercase words as the same word, and handle rows that contain missing text (NULL/None).",
                "hint": "Python: Drop missing rows using `.dropna()`, convert to lowercase `.str.lower()`. SQL: Use `LOWER()` and filter with `WHERE text IS NOT NULL`.",
                "data": pd.DataFrame({
                    "text": ["The sunny day", "is Sunny and the", None, "day Is good"]
                }),
                "evaluation_criteria": [
                    "String normalization (lowercasing)",
                    "Robustness against null values in aggregation inputs"
                ],
                "solution_code": """\
from collections import Counter
import pandas as pd

# Handle nulls and uppercase
all_text = " ".join(df["text"].dropna().str.lower().tolist())
word_counts = Counter(all_text.split())

result = pd.DataFrame(word_counts.items(), columns=["word", "frequency"])
result = result.sort_values(by=["frequency", "word"], ascending=[False, True]).reset_index(drop=True)
""",
                "solution_sql": """\
WITH SplitWords AS (
    SELECT unnest(string_split(LOWER(text), ' ')) AS word
    FROM documents
    WHERE text IS NOT NULL
)
SELECT 
    word,
    COUNT(*) AS frequency
FROM SplitWords
GROUP BY word
ORDER BY frequency DESC, word ASC;
""",
                "expected_output": pd.DataFrame({
                    "word": ["day", "is", "sunny", "the", "and", "good"],
                    "frequency": [2, 2, 2, 2, 1, 1]
                }),
                "follow_up_probes": [
                    "What happens if there are Leading or Trailing spaces before/after missing data handling?",
                    "How would this change if we needed to preserve case for display but count them together?"
                ]
            },
            {
                "stage_number": 4,
                "title": "Punctuation & Irregular Spacing",
                "scenario": "Text frequently contains punctuation marks and multiple spaces. Strip out all punctuation before counting and ensure extra spaces don't produce empty words.",
                "hint": "Python: Use `re.sub(r'[^\\w\\s]', '', text)` to remove punctuation. SQL: Use `regexp_replace(text, '[^a-zA-Z0-9\\s]', '', 'g')`.",
                "data": pd.DataFrame({
                    "text": ["The sunny day!", "is Sunny, and the...", None, "day Is good.", "  extra   spaces  "]
                }),
                "evaluation_criteria": [
                    "Familiarity with Regex for basic text cleaning",
                    "Properly filtering out empty strings caused by extra spaces"
                ],
                "solution_code": """\
import re
from collections import Counter
import pandas as pd

all_text = " ".join(df["text"].dropna().str.lower().tolist())

# Remove punctuation
clean_text = re.sub(r'[^\\w\\s]', '', all_text)

word_counts = Counter(clean_text.split())

result = pd.DataFrame(word_counts.items(), columns=["word", "frequency"])
result = result.sort_values(by=["frequency", "word"], ascending=[False, True]).reset_index(drop=True)
""",
                "solution_sql": """\
WITH CleanedText AS (
    SELECT text
    FROM documents
    WHERE text IS NOT NULL
),
ReplacedText AS (
    SELECT regexp_replace(LOWER(text), '[^a-z0-9\\s]', '', 'g') AS clean_text
    FROM CleanedText
),
SplitWords AS (
    SELECT unnest(string_split(clean_text, ' ')) AS word
    FROM ReplacedText
)
SELECT 
    word,
    COUNT(*) AS frequency
FROM SplitWords
WHERE word != ''
GROUP BY word
ORDER BY frequency DESC, word ASC;
""",
                "expected_output": pd.DataFrame({
                    "word": ["day", "is", "sunny", "the", "and", "extra", "good", "spaces"],
                    "frequency": [2, 2, 2, 2, 1, 1, 1, 1]
                }),
                "follow_up_probes": [
                    "What kind of performance impact does the regex replacement introduce?",
                    "How would you handle word variations like 'run', 'running', 'ran' (stemming/lemmatization) if requested later?"
                ]
            }
        ]
    }
