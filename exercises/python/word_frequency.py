import pandas as pd
from collections import Counter

def get_exercise():
    return {
        "title": "Word Frequency",
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
        "deep_dive": "Joining the entire column into a single string heavily allocates memory, but allows Python's `.split()` to parse all tokens in one pass via C. The `collections.Counter()` is a specialized dictionary designed precisely for multiset counting, hashing each word in O(1) time. Overall time complexity is linear O(N) relative to the total number of characters across all rows."
    }
