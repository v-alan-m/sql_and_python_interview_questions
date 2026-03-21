import pandas as pd

def get_exercise():
    return {
        "title": "Cumulative Revenue",
        "subtitle": "Window Functions, GROUP BY, Common Table Expressions (CTEs), Pandas Aggregation",
        "description": "Calculate the running total (cumulative sum) of revenue chronologically. The dataset contains 'date' and 'daily_revenue'.",
        "data": pd.DataFrame({
            "date": ["2023-01-03", "2023-01-01", "2023-01-04", "2023-01-02"],
            "daily_revenue": [150, 100, 300, 250]
        }),
        "table_name": "daily_sales",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "First, make sure your data is sorted correctly by the date column. Then, use the `.cumsum()` method on the revenue column.",
        "hint_sql": "Use the `SUM()` aggregate function but apply it as a window function using an `OVER()` clause that orders by date.",
        "solution_python": """
# Ensure the dataframe is chronologically sorted first
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# Calculate running total
df["cumulative_revenue"] = df["daily_revenue"].cumsum()
result = df
""",
        "solution_sql": """
SELECT 
    date, 
    daily_revenue, 
    SUM(daily_revenue) OVER (ORDER BY date ASC) AS cumulative_revenue
FROM daily_sales
ORDER BY date ASC;
""",
        "deep_dive": "Window functions in SQL and the `.cumsum()` method in Pandas process sequential operations effectively. Sorting the dataset is universally the bottleneck here, taking O(N log N) time, while the cumulative calculation itself runs in linear O(N) time. The overall time complexity is therefore O(N log N). Omitting the `ORDER BY` in SQL's `OVER()` clause would compute a total sum instead of a running sum.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Already Sorted Data",
                "scenario": "Let's start with a simplified version. Suppose we have a dataframe containing our daily revenue, and it is already perfectly sorted chronologically. Can you calculate the running total of revenue for each row?",
                "hint": "You can use the `.cumsum()` method directly on the revenue column.",
                "data": pd.DataFrame({
                    "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
                    "daily_revenue": [100, 250, 150, 300]
                }),
                "evaluation_criteria": [
                    "Knowledge of standard Pandas window/cumulative functions.",
                    "Clean and direct assignment to a new column."
                ],
                "solution_code": """\
df["cumulative_revenue"] = df["daily_revenue"].cumsum()
result = df""",
                "solution_sql": """\
SELECT 
    date, 
    daily_revenue, 
    SUM(daily_revenue) OVER (ORDER BY date ASC) AS cumulative_revenue
FROM daily_sales
ORDER BY date ASC;""",
                "expected_output": pd.DataFrame({
                    "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
                    "daily_revenue": [100, 250, 150, 300],
                    "cumulative_revenue": [100, 350, 500, 800]
                }),
                "follow_up_probes": [
                    "Time Complexity: What is the time complexity of the cumulative sum operation under the hood?",
                    "Alternative Approaches: How would you achieve this if you were iterating with standard Python lists instead of using Pandas?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Out-of-Order Dates",
                "scenario": "In reality, the data pipeline doesn't guarantee the order of the records, and the dates might be loaded as strings in random order. How would you update your logic to ensure the running total is correctly calculated chronologically?",
                "hint": "You will need to cast the date strings to proper datetime objects so they can be sorted reliably before computing the cumulative sum.",
                "data": pd.DataFrame({
                    "date": ["2023-01-03", "2023-01-01", "2023-01-04", "2023-01-02"],
                    "daily_revenue": [150, 100, 300, 250]
                }),
                "evaluation_criteria": [
                    "Ability to safely cast data types in Pandas (`pd.to_datetime`).",
                    "Sorting operations and resetting index if necessary."
                ],
                "solution_code": """\
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)
df["cumulative_revenue"] = df["daily_revenue"].cumsum()
result = df""",
                "solution_sql": """\
SELECT 
    date, 
    daily_revenue, 
    SUM(daily_revenue) OVER (ORDER BY date ASC) AS cumulative_revenue
FROM daily_sales
ORDER BY date ASC;""",
                "expected_output": pd.DataFrame({
                    "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"]),
                    "daily_revenue": [100, 250, 150, 300],
                    "cumulative_revenue": [100, 350, 500, 800]
                }),
                "follow_up_probes": [
                    "Resetting Index: Why might `reset_index(drop=True)` be a good practice after sorting dataframes in Pandas?",
                    "Performance: What is the computational bottleneck of our solution now?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Multiple Entries Per Day",
                "scenario": "Our system logs multiple transactions over the course of a day, meaning some dates appear more than once. We need the daily cumulative revenue. Modify your logic to group multiple entries on the same day into a single daily total before running the cumulative sum.",
                "hint": "You need an aggregation step (e.g., `groupby().sum()`) on the dates to flatten the data to one row per day before you sort and apply `.cumsum()`.",
                "data": pd.DataFrame({
                    "date": ["2023-01-01", "2023-01-02", "2023-01-02", "2023-01-03"],
                    "daily_revenue": [100, 150, 100, 150]
                }),
                "evaluation_criteria": [
                    "Mastery of SQL-like aggregation patterns in Pandas (`groupby`).",
                    "Handling of DataFrame shapes and indices during analytical pipelines."
                ],
                "solution_code": """\
df["date"] = pd.to_datetime(df["date"])
df = df.groupby("date", as_index=False)["daily_revenue"].sum()
df = df.sort_values("date").reset_index(drop=True)
df["cumulative_revenue"] = df["daily_revenue"].cumsum()
result = df""",
                "solution_sql": """\
WITH DailyTotals AS (
    SELECT 
        date,
        SUM(daily_revenue) AS daily_revenue
    FROM daily_sales
    GROUP BY date
)
SELECT 
    date,
    daily_revenue,
    SUM(daily_revenue) OVER (ORDER BY date ASC) AS cumulative_revenue
FROM DailyTotals
ORDER BY date ASC;""",
                "expected_output": pd.DataFrame({
                    "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
                    "daily_revenue": [100, 250, 150],
                    "cumulative_revenue": [100, 350, 500]
                }),
                "follow_up_probes": [
                    "Datetime Grouping: If our dates included time components (`2023-01-01 14:05:00`), how would you group by just the calendar day?",
                    "Missing Days: What if there were days with zero transactions, and we wanted every calendar day represented? How would you fill those gaps?"
                ]
            }
        ]
    }
