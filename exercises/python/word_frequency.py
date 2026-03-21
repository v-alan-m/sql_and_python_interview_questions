import pandas as pd
from collections import Counter

def get_exercise():
    return {
        "title": "Word Frequency",
        "subtitle": "Loops, Arrays / Lists, Hash Maps / Dictionaries, Sets",
        "description": "Given a column containing sentences, determine the frequency of each unique word across the entire column. A word is defined as a sequence of non-space characters. Return a dictionary mapping words to their integer counts, ignoring case.",
        "data": pd.DataFrame({
            "sentence": [
                "The day is sunny the the",
                "the sunny is is"
            ]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Standardize the string case first (e.g. `.lower()`). Join all the sentences into one massive string, then split it into a list of words. Feed this list into `collections.Counter()`.",
        "hint_sql": "",
        "solution_python": '''\nfrom collections import Counter\n\ndef get_total_word_frequencies(df_series):\n    # 1. Join all strings with a space\n    all_text = " ".join(df_series)\n    \n    # 2. Lowercase and split into words\n    words = all_text.lower().split()\n    \n    # 3. Use Counter to get frequencies\n    return dict(Counter(words))\n\nword_freqs = get_total_word_frequencies(df["sentence"])\nresult = word_freqs\n''',
        "solution_sql": "",
        "deep_dive": "Joining the entire column into a single string heavily allocates memory, but allows Python's `.split()` to parse all tokens in one pass via C. The `collections.Counter()` is a specialized dictionary designed precisely for multiset counting, hashing each word in O(1) time. Overall time complexity is linear O(N) relative to the total number of characters across all rows.",
        "big_o_explanation": "### ⏱️ Optimal Big O Notation\n**Time Complexity:** `O(N)` where N is the total number of characters across all text. Splitting, lowercasing, and counting all take linear time.\n**Space Complexity:** `O(N + U)` where `N` is the string size (to store the string copies and the split list of words) and `U` is the number of unique words returned in the Counter hash map.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Single Sentence",
                "scenario": "Let's start simple. Given a DataFrame with a single row containing a sentence, can you return a dictionary mapping each word to its frequency? A word is separated by spaces.",
                "hint": "You can access the first row's string, use `.split()` to break it into words, and feed it into `collections.Counter()`.",
                "data": pd.DataFrame({"sentence": ["apple orange apple banana"]}),
                "evaluation_criteria": [
                    "Basic string manipulation (`.split()`)",
                    "Counting frequencies using either a loop with a standard dictionary or `collections.Counter`"
                ],
                "solution_code": """\
from collections import Counter
text = df["sentence"].iloc[0]
result = dict(Counter(text.split()))""",
                "expected_output": {'apple': 2, 'orange': 1, 'banana': 1},
                "follow_up_probes": [
                    "What is the time complexity of your solution?",
                    "If we couldn't use `collections.Counter`, how would you implement the frequency counting manually using a standard dictionary?"
                ],
                "big_o_explanation": "#### Stage 1: Single Sentence\n**Time Complexity:** `O(N)` where `N` is the characters in the string. Iterating via `.split()` takes `O(N)`, and hashing into `Counter` takes `O(N)`.\n**Space Complexity:** `O(W)` where `W` is the number of words. The `.split()` method creates a new list containing all `W` words, and `Counter` creates a dictionary mapping the unique words to integers."
            },
            {
                "stage_number": 2,
                "title": "Multiple Sentences",
                "scenario": "Good. Now the DataFrame column `sentence` contains multiple rows. We need the total word frequency across all the rows combined.",
                "hint": "You need to combine all the strings in the column into one large string before splitting, or split each row and aggregate the results. Joining using `\" \".join()` is usually the cleanest approach.",
                "data": pd.DataFrame({
                    "sentence": [
                        "apple orange",
                        "apple banana",
                        "orange"
                    ]
                }),
                "evaluation_criteria": [
                    "Aggregating strings across a pandas Series (e.g. `' '.join(df_series)`)",
                    "Handling multi-row context"
                ],
                "solution_code": """\
from collections import Counter
all_text = " ".join(df["sentence"])
result = dict(Counter(all_text.split()))""",
                "expected_output": {'apple': 2, 'orange': 2, 'banana': 1},
                "follow_up_probes": [
                    "Are there alternative ways to solve this besides joining all strings first? (e.g., iterating over rows and updating a counter).",
                    "What are the memory implications of joining all sentences into one massive string versus processing row-by-row?"
                ],
                "big_o_explanation": "#### Stage 2: Multiple Sentences\n**Time Complexity:** `O(N)`. Joining the strings is `O(N)`, and then splitting and counting remains `O(N)` relative to total character count.\n**Space Complexity:** `O(N)`. `\" \".join()` creates a brand-new string in memory containing all the text, which doubles the immediate memory footprint before the word list is even built."
            },
            {
                "stage_number": 3,
                "title": "Case Insensitivity",
                "scenario": "Words are now appearing with different capitalisations, but we want the counts to be case-insensitive (so 'Apple' and 'apple' count as the same word).",
                "hint": "Standardize the casing of the combined text using `.lower()` before you split it into words.",
                "data": pd.DataFrame({
                    "sentence": [
                        "Apple orange",
                        "apple Banana",
                        "ORANGE"
                    ]
                }),
                "evaluation_criteria": [
                    "String casing normalization before tokenization"
                ],
                "solution_code": """\
from collections import Counter
all_text = " ".join(df["sentence"])
words = all_text.lower().split()
result = dict(Counter(words))""",
                "expected_output": {'apple': 2, 'orange': 2, 'banana': 1},
                "follow_up_probes": [
                    "Why is it better to call `.lower()` on the combined string rather than on each word individually after splitting?"
                ],
                "big_o_explanation": "#### Stage 3: Case Insensitivity\n**Time Complexity:** `O(N)`. `.lower()` adds another full string traversal but overall it remains `O(N)`.\n**Space Complexity:** `O(N)`. Because strings in Python are immutable, calling `.lower()` instantiates another completely new, full-length string in memory."
            },
            {
                "stage_number": 4,
                "title": "Stop Words Filter",
                "scenario": "Finally, we want to ignore common 'stop words'. Modify your solution to exclude the words `'is'`, `'the'`, and `'a'` from the final frequency count.",
                "hint": "You'll need a conditional check while processing your words. A list comprehension or a loop that checks if each word is `not in` a predefined set of stop words works well.",
                "data": pd.DataFrame({
                    "sentence": [
                        "The apple is orange",
                        "A banana",
                        "apple"
                    ]
                }),
                "evaluation_criteria": [
                    "Conditional iteration (filtering specific items during processing)",
                    "Using sets for O(1) membership lookups"
                ],
                "solution_code": """\
from collections import Counter
stop_words = {"is", "the", "a"}
all_text = " ".join(df["sentence"]).lower()
valid_words = [w for w in all_text.split() if w not in stop_words]
result = dict(Counter(valid_words))""",
                "expected_output": {'apple': 2, 'orange': 1, 'banana': 1},
                "follow_up_probes": [
                    "Why should `stop_words` be defined as a set rather than a list? How does this affect time complexity?",
                    "How would your code handle punctuation attached to a stop word, e.g., `\"the,\"`? (Note: It's fine if it doesn't currently, just explain what would happen)."
                ],
                "big_o_explanation": "#### Stage 4: Stop Words Filter\n**Time Complexity:** `O(N)`. Checking membership in the `stop_words` set is `O(1)`, so applying it as a filter across the list of words adds no significant algorithmic overhead.\n**Space Complexity:** `O(N + K)` where `K` is the small constant size of the stop words set."
            }
        ]
    }
