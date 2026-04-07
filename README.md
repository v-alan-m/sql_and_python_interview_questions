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

*  **3-Way Quick Sort (Dutch National Flag):** A specific pointer-manipulation trick not commonly used over basic Quick Sort.

*   **In-Place Merge Sort:** Extremely complex pointer/index management that tests deep systems knowledge rather than Python/Data skills.

*   **Binary Insertion Sort:** Considered too academic.

*   **Sorting Linked Lists:** DEs almost always use Arrays/Lists or DataFrames. Having to sort a custom-built Singly Linked List is a classic SWE question that rarely applies to DE scenarios.

*   **Radix / Bucket Sort Variations (Strings/Negatives):** Radix and Bucket sorts are already niche. Being asked to modify them for negative numbers or alphabetizing strings is very low probability for a DE role.

## Real World Scenarios

This repository also contains a curated suite of **Real-World Data Engineering Scenarios** modeled after actual interview questions from top tech companies (Meta, Netflix, Stripe, etc.). These exercises focus on practical data pipeline and modeling concepts rather than pure algorithms.

### Available Scenarios:

1. **User Growth Analytics Dashboard:** Star schema design, cumulative aggregation, and channel-segmented growth.
2. **E-Commerce Order Pipeline:** Idempotent deduplication, handling late-arriving data, and batch vs. streaming concepts.
3. **Platform Engagement (Gaps & Islands):** Sessionization, consecutive login streaks, and cohort analysis.
4. **Data Quality & Pipeline Monitoring:** Anomaly detection (Z-scores), circuit breakers, and null/duplicate rate monitoring.
5. **Revenue Data Warehouse:** Dimensional modeling, fact/dimension tables, and Slowly Changing Dimensions (SCD Type 2).

### Running a Scenario

You can interact with these scenarios directly in the Streamlit app. They are marked under the "Real-World Scenarios" category. The application will present you with business context, a simulated schema, and progressive tasks ranging from Entry to Senior DE levels.
