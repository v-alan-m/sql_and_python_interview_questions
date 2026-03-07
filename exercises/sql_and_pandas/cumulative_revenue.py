import pandas as pd

def get_exercise():
    return {
        "title": "Cumulative Revenue",
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
        "deep_dive": "Window functions in SQL and the `.cumsum()` method in Pandas process sequential operations effectively. Sorting the dataset is universally the bottleneck here, taking O(N log N) time, while the cumulative calculation itself runs in linear O(N) time. The overall time complexity is therefore O(N log N). Omitting the `ORDER BY` in SQL's `OVER()` clause would compute a total sum instead of a running sum."
    }
