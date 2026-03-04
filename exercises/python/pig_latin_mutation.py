import pandas as pd

def get_exercise():
    return {
        "title": "Pig Latin Mutation",
        "description": "Given a Pandas DataFrame containing a column 'word', write a Python script to mutate each word into its Pig Latin equivalent. For words that begin with consonants, all letters before the initial vowel are placed at the end of the word sequence, followed by 'ay'. For words that begin with vowels, simply add 'yay' to the end.",
        "data": pd.DataFrame({
            "word": ["hello", "apple", "strong", "idea", "rhythm"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "Define a helper logic function to process a single string. Find the index of the first vowel, slice the string accordingly, and append the appropriate suffix. Apply this function to the DataFrame column.",
        "hint_sql": "Not applicable",
        "solution_python": """
def to_pig_latin(word):
    vowels = "aeiouAEIOU"
    if word[0] in vowels:
        return word + "yay"
        
    for i, char in enumerate(word):
        if char in vowels:
            return word[i:] + word[:i] + "ay"
            
    # Fallback for words without standard vowels like 'rhythm'
    return word + "ay"

df["pig_latin"] = df["word"].apply(to_pig_latin)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "Pandas' `.apply()` method is highly versatile but fundamentally acts as a Python-level loop over the data. The time complexity for the string mutation is O(N * M) where N is the number of rows and M is the average word length. For very large datasets, using vectorized string methods (e.g., regex via `df['word'].str.extract()`) could be slightly faster, but custom string manipulation often relies on `.apply() ` for readability."
    }
