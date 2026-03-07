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
