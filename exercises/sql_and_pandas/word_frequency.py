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
        "big_o_explanation": "Time Complexity: O(N) where N is the total number of characters across all words. Python's `string.split()` plus `collections.Counter` iterates over the string linearly to tokenize and hash. Sorting the final unique vocabulary takes O(V log V) where V is the number of unique words. Space Complexity: O(V) to store the vocabulary frequencies in the dictionary. Hashing string chunks continuously is the primary optimization rather than nested loop searching for word occurrences.",
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
                "big_o_explanation": "Time Complexity: O(N + V log V). Splitting and traversing the string is O(N) for string length N. Counting is O(N). Sorting the resulting V unique words is O(V log V). Space Complexity: O(V) for the frequency dictionary structure. Using built-in hash maps like Python's `Counter` directly optimizes the frequency aggregation over manual list counting.",
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
                "big_o_explanation": "Time Complexity: O(N + V log V). Concatenating all text first takes O(N). Hashing is O(N). SQL handles this similarly by scanning each un-nested row and aggregating them via a hash/sort group by. Space Complexity: O(N) for creating the concatenated string in Python, plus O(V) for unique word counts. Concatenation allows a single continuous chunking action instead of looping repeatedly per document.",
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
                "big_o_explanation": "Time Complexity: O(N + V log V). Applying `.dropna()` and `.str.lower()` adds O(N) linear passes over the characters to standardize them before counting. Space Complexity: O(N) for the cleaned string copies in memory. While we do an extra pass over the data, linear passes scale excellently, and cleaning standardizes the dictionary hash space, likely reducing V (unique words).",
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
                "big_o_explanation": "Time Complexity: O(N + V log V). Regular Expression substitutions add a heavy constant factor to the O(N) traversal for string cleanup, scanning each character for punctuation matches. Overall complexity remains linear with respect to text length. Space Complexity: O(N) to hold string copies during text mutation. Batching transformations (lower-casing, regex replacement) iteratively keeps memory bounds linear instead of blowing up memory with Cartesian character matches.",
                "follow_up_probes": [
                    "What kind of performance impact does the regex replacement introduce?",
                    "How would you handle word variations like 'run', 'running', 'ran' (stemming/lemmatization) if requested later?"
                ]
            }
        ]
    }
