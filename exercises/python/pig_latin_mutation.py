import pandas as pd

def get_exercise():
    return {
        "title": "Pig Latin Mutation",
        "subtitle": "Loops, Arrays / Lists, Sets",
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
        "deep_dive": "Pandas' `.apply()` method is highly versatile but fundamentally acts as a Python-level loop over the data. The time complexity for the string mutation is O(N * M) where N is the number of rows and M is the average word length. For very large datasets, using vectorized string methods (e.g., regex via `df['word'].str.extract()`) could be slightly faster, but custom string manipulation often relies on `.apply() ` for readability.",
        "big_o_explanation": "Time Complexity: O(N * M) where N is the number of rows (words) in the dataset and M is the average length of a word. `.apply()` runs the function sequentially on each row. Searching for vowels takes O(M) time per word in the worst case. Space Complexity: O(N * M) to allocate the new 'pig_latin' column in the Pandas DataFrame.",

        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Vowel-Start Words Only",
                "scenario": "You receive a DataFrame with a column 'word'. Every word starts with a vowel. Convert each to Pig Latin by appending 'yay'.",
                "hint": "Define a simple helper function that takes a single word and returns word + 'yay'. Apply it to the DataFrame column using .apply().",
                "data": pd.DataFrame({
                    "word": ["apple", "idea", "orange"]
                }),
                "evaluation_criteria": [
                    "Can the candidate write a basic helper function?",
                    "Can they use df.apply() correctly?",
                    "Do they handle case sensitivity (vowel set includes upper/lowercase)?"
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({"word": ["apple", "idea", "orange"]})

def to_pig_latin(word):
    return word + "yay"

df["pig_latin"] = df["word"].apply(to_pig_latin)
result = df
print(result)""",
                "expected_output": pd.DataFrame({
                    "word": ["apple", "idea", "orange"],
                    "pig_latin": ["appleyay", "ideayay", "orangeyay"]
                }),
                "big_o_explanation": "Time Complexity: O(N * M) where N is the number of words and M is the word length. Pandas `.apply()` executes the Python logic row-by-row. Space Complexity: O(N * M) to create and store the new strings in the DataFrame column. String concatenation `+` for small strings is heavily optimized in Python.",
                "follow_up_probes": [
                    "Why did you choose .apply() over a list comprehension here?",
                    "What's the time complexity of this approach? → O(N), one pass over rows."
                ]
            },
            {
                "stage_number": 2,
                "title": "Multi-Word Phrases with Capitalisation",
                "scenario": "Now the data contains phrases of two words, and some words are capitalised (e.g., 'Hello World'). Each word should be converted independently. The result must preserve the original capitalisation pattern — if the original word was capitalised, the Pig Latin result should also start with a capital letter and the rest lowercase.",
                "hint": "Split the phrase on spaces, process each word individually, then rejoin with ' '.join(). To handle capitalisation: check if the original word starts uppercase with .isupper(), convert to lowercase for processing, then re-capitalise the result with .capitalize() if needed.",
                "data": pd.DataFrame({
                    "phrase": ["Hello World", "apple Pie", "Strong Coffee", "Open idea"]
                }),
                "evaluation_criteria": [
                    "Can the candidate split a phrase, process each word, and rejoin?",
                    "Capitalisation transfer: 'Hello' → 'Ellohay' (capital moves to new first letter)",
                    "String method awareness: .capitalize(), .lower(), .isupper()"
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({
    "phrase": ["Hello World", "apple Pie", "Strong Coffee", "Open idea"]
})

def to_pig_latin_word(word):
    vowels = "aeiouAEIOU"
    is_cap = word[0].isupper()

    lower_word = word.lower()

    if lower_word[0] in "aeiou":
        result = lower_word + "yay"
    else:
        for i, char in enumerate(lower_word):
            if char in "aeiou":
                result = lower_word[i:] + lower_word[:i] + "ay"
                break
        else:
            result = lower_word + "ay"

    return result.capitalize() if is_cap else result

def to_pig_latin_phrase(phrase):
    return " ".join(to_pig_latin_word(w) for w in phrase.split())

df["pig_latin"] = df["phrase"].apply(to_pig_latin_phrase)
result = df
print(result)""",
                "expected_output": pd.DataFrame({
                    "phrase": ["Hello World", "apple Pie", "Strong Coffee", "Open idea"],
                    "pig_latin": ["Ellohay Orldway", "appleyay Iepay", "Ongstray Offeecay", "Openyay ideayay"]
                }),
                "big_o_explanation": "Time Complexity: O(N * M) overall, because splitting the phrase, iterating characters to find a vowel, and slicing strings all operate proportionally to the phrase length M. Space Complexity: O(N * M) for the newly constructed strings and intermediate lists created by `.split()`. Converting to lowercase first prevents repeated `.lower()` calls and simplifies the condition checks.",
                "follow_up_probes": [
                    "Walk through 'apple Pie' step by step. → 'apple' starts lowercase + vowel → 'appleyay'. 'Pie' is capitalised + consonant → 'ie' + 'p' + 'ay' = 'iepay' → capitalise → 'Iepay'.",
                    "What if a word is ALL CAPS like 'NASA'? → Tests whether the candidate would extend to a full-caps branch.",
                    "Why convert to lowercase first before processing? → Simplifies vowel-checking logic; capitalisation is re-applied at the end."
                ]
            },
            {
                "stage_number": 3,
                "title": "Edge Cases, Punctuation & Robustness",
                "scenario": "Final round. The data now includes punctuation (e.g., 'Hello, World!'), no-vowel words (e.g., 'Rhythm'), and potentially empty strings. Handle all edge cases cleanly.",
                "hint": "Before processing a word, strip any trailing non-alpha characters (e.g., !, ,, .) into a suffix variable using a while loop. Process the clean word normally, then reattach the suffix at the end. Add an early return for empty or whitespace-only strings.",
                "data": pd.DataFrame({
                    "phrase": ["Hello, World!", "Strong Rhythm", "Open idea", "", "apple Pie."]
                }),
                "evaluation_criteria": [
                    "Punctuation stripping and reattachment",
                    "No-vowel fallback ('rhythm' → 'rhythmay')",
                    "Empty/whitespace-only input guard",
                    "Code extensibility — how much of Stage 2 survives intact?"
                ],
                "solution_code": """\
import pandas as pd

df = pd.DataFrame({
    "phrase": ["Hello, World!", "Strong Rhythm", "Open idea", "", "apple Pie."]
})

def to_pig_latin_word(word):
    if not word:
        return word

    # Strip trailing punctuation
    suffix = ""
    while word and not word[-1].isalpha():
        suffix = word[-1] + suffix
        word = word[:-1]

    if not word:
        return suffix

    is_cap = word[0].isupper()
    lower_word = word.lower()

    if lower_word[0] in "aeiouy":
        result = lower_word + "yay"
    else:
        for i, char in enumerate(lower_word):
            if char in "aeiouy":
                result = lower_word[i:] + lower_word[:i] + "ay"
                break
        else:
            # No vowels (edge case, not physically possible if 'y' is a vowel)
            result = lower_word + "ay"

    result = result.capitalize() if is_cap else result
    return result + suffix

def to_pig_latin_phrase(phrase):
    if not phrase or not phrase.strip():
        return phrase
    return " ".join(to_pig_latin_word(w) for w in phrase.split())

df["pig_latin"] = df["phrase"].apply(to_pig_latin_phrase)
result = df
print(result)""",
                "expected_output": pd.DataFrame({
                    "phrase": ["Hello, World!", "Strong Rhythm", "Open idea", "", "apple Pie."],
                    "pig_latin": ["Ellohay, Orldway!", "Ongstray Ythmrhay", "Openyay ideayay", "", "appleyay Iepay."]
                }),
                "big_o_explanation": "Time Complexity: O(N * M). The additional while-loop to strip punctuation also runs in O(M) time, keeping the asymptotic time bound the same. Space Complexity: O(N * M). The heavy memory allocation is mostly from the DataFrame. While cleanly factored, `.apply()` on millions of rows is slow because it cannot vectorize these custom Python operations; for massive data, Regex replacement or parallelization tools like Dask would be required.",
                "follow_up_probes": [
                    "How much code changed from Stage 2? → Only the punctuation handling wrapper and the empty-string guard. Core logic stayed intact.",
                    "Time complexity? → O(N × M) where N = rows, M = avg word length.",
                    "At 10 million rows, how would you optimise? → Vectorised regex via df['phrase'].str.replace(), or chunked .apply() with Dask for parallelism."
                ]
            }
        ]
    }
