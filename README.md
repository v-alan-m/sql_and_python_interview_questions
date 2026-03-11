# Sql and Python Interview Questions

## Run appplication

- `streamlit run sql_and_python_interview_questions.py`

## Type into app's text area:
```python
def reverse_func(s):
    return " ".join(s.split()[::-1])

result = df['sentences'].apply(reverse_func)
```

## Automated Tests

- Run python test_all_exercises.py 
- To verify that:
    - The output cleanly parses through all known exercises without encountering loading errors.
- Accurately summarizes the test results.

## Additional Algos

The following algorithms are **unlikely** to appear in a Data Engineering interview, as they lean heavily towards pure Software Engineering or academic concepts rather than testing data pipeline/streaming logic:

*   **3-Way Quick Sort (Dutch National Flag):** A specific pointer-manipulation trick not commonly used over basic Quick Sort.
*   **In-Place Merge Sort:** Extremely complex pointer/index management that tests deep systems knowledge rather than Python/Data skills.
*   **Binary Insertion Sort:** Considered too academic.
*   **Sorting Linked Lists:** DEs almost always use Arrays/Lists or DataFrames. Having to sort a custom-built Singly Linked List is a classic SWE question that rarely applies to DE scenarios.
*   **Radix / Bucket Sort Variations (Strings/Negatives):** Radix and Bucket sorts are already niche. Being asked to modify them for negative numbers or alphabetizing strings is very low probability for a DE role.
