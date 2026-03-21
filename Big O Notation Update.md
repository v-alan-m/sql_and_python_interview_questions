# System Prompt: Incrementally Adding Big O Notation & Explanations

## Context
We are upgrading a coding interview application built in Streamlit. The goal is to add a new feature that tracks and cumulatively displays the **Big O Notation & Optimization** explanation as users progress through the interview stages of various Python, SQL, and Sorting Algorithm exercises. 

Because modifying ~45 files at once leads to AI context rot, we are batching the changes. You will process exactly **5 exercises at a time** from the list below.

## Core Tasks

### Task 1: Streamlit UI Update (Run Once)
Before updating any exercises, ensure that `sql_and_python_interview_questions.py` has been updated to include the new UI logic. 
- Add a new `st.expander("⏱️ Big O Notation & Optimization")` right after the "💬 Follow-Up Probes" expander (or wherever appropriate in the UI).
- The dropdown MUST be **cumulative**.
- **Crucial Logic**: If the user is on Stage `N`, the expander should display the `big_o_explanation` from Stage `1`, Stage `2`, up to Stage `N`. It should concatenate them together using Markdown headers like `#### Stage 1 Approach`, `#### Stage 2 Optimization`, etc.

### Task 2: Update 5 Exercises per Session
Look at the `## Exercise Tracking List` below. Find the first 5 contiguous unchecked (`[ ]`) exercises.
For **each** of those 5 files:
1. Examine the base exercise and the `interview_stages` dictionaries.
2. Generate a detailed, educational `"big_o_explanation"` for the base problem and for every stage.
   - **Content:** The explanation MUST explain exactly what the Time and Space complexity is (e.g., O(N)), *why* it is that complexity, and *how* the specific approach used in that stage optimizes the problem compared to naive approaches.
3. Inject the `"big_o_explanation"` key into the base exercise dict, and into each dict inside the `interview_stages` list.
4. **Important**: You must make sure there are no syntax errors introduced into the Python dictionaries. Use `replace_file_content` or `multi_replace_file_content` to surgically inject the keys.

### Task 3: Test and Update Tracking
1. After updating the 5 files, run `python test_all_exercises.py` to ensure unit tests still pass and no syntax errors were introduced.
2. Mark the 5 files you completed as `[x]` in the `## Exercise Tracking List` inside **this exact system prompt file**.
3. Reply to the user summarizing what concepts were documented, and ask them to type `"next"` to process the next set of 5.

---

## Exercise Tracking List

- [x] exercises/python/anagram_checker.py
- [x] exercises/python/caesar_cipher.py
- [x] exercises/python/first_unique_character.py
- [x] exercises/python/isomorphic_strings.py
- [x] exercises/python/keyboard_row.py
- [x] exercises/python/last_word_length.py
- [x] exercises/python/longest_common_prefix.py
- [x] exercises/python/palindrome_logic.py
- [x] exercises/python/permutations.py
- [x] exercises/python/pig_latin_mutation.py
- [x] exercises/python/remove_duplicates.py
- [x] exercises/python/reverse_words.py
- [x] exercises/python/roman_to_int.py
- [x] exercises/python/string_compression.py
- [x] exercises/python/string_rotation.py
- [x] exercises/python/title_case_manual.py
- [x] exercises/python/urlify.py
- [x] exercises/python/valid_parentheses.py
- [x] exercises/python/vowel_counter.py
- [x] exercises/python/word_frequency.py
- [x] exercises/python/zigzag_conversion.py
- [x] exercises/sorting_algorithms/de_algos/merge_k_sorted_arrays.py
- [x] exercises/sorting_algorithms/de_algos/min_max_heap.py
- [x] exercises/sorting_algorithms/de_algos/sorting_objects.py
- [x] exercises/sorting_algorithms/de_algos/top_k_elements.py
- [x] exercises/sorting_algorithms/entry_algos/bubble_sort.py
- [x] exercises/sorting_algorithms/entry_algos/insertion_sort.py
- [x] exercises/sorting_algorithms/entry_algos/selection_sort.py
- [x] exercises/sorting_algorithms/entry_algos/stable_selection_sort.py
- [x] exercises/sorting_algorithms/mid_algos/iterative_merge_sort.py
- [x] exercises/sorting_algorithms/mid_algos/merge_sort.py
- [x] exercises/sorting_algorithms/mid_algos/quick_select.py
- [x] exercises/sorting_algorithms/mid_algos/quick_sort.py
- [x] exercises/sorting_algorithms/senior_algos/bucket_sort.py
- [x] exercises/sorting_algorithms/senior_algos/heap_sort.py
- [x] exercises/sorting_algorithms/senior_algos/radix_sort.py
- [x] exercises/sql_and_pandas/cumulative_revenue.py
- [x] exercises/sql_and_pandas/daily_price_delta.py
- [x] exercises/sql_and_pandas/deduplication.py
- [x] exercises/sql_and_pandas/gaps_and_islands.py
- [x] exercises/sql_and_pandas/last_word_length.py
- [x] exercises/sql_and_pandas/longest_common_prefix.py
- [x] exercises/sql_and_pandas/remove_duplicates.py
- [x] exercises/sql_and_pandas/word_frequency.py
