import pandas as pd

def get_exercise():
    return {
        "title": "Gaps and Islands",
        "description": "The 'Gaps and Islands' problem involves grouping sequential dates or numbers together into 'islands' and treating non-sequential breaks as 'gaps'. Given a sequence of dates where a user was active, find the start and end date for each continuous streak of activity.",
        "data": pd.DataFrame({
            "user_id": [1, 1, 1, 1, 1, 2, 2],
            "active_date": [
                "2023-01-01", "2023-01-02", "2023-01-03", 
                "2023-01-06", "2023-01-07", 
                "2023-02-01", "2023-02-05"
            ]
        }),
        "table_name": "user_activity",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "Calculate the difference in days between the current row and the previous row using `.diff()`. Where the difference is > 1 day, it marks the start of a new island. Assign a cumulative ID to group by.",
        "hint_sql": "Use the `ROW_NUMBER()` trick: subtract the row number (as integer days) from the date. Sequential dates will yield the same 'baseline' date, which can then be used to `GROUP BY`.",
        "solution_python": """
df["active_date"] = pd.to_datetime(df["active_date"])

# Ensure data is sorted
df = df.sort_values(by=["user_id", "active_date"])

# 1. Calculate difference between current date and previous date per user
df["date_diff"] = df.groupby("user_id")["active_date"].diff().dt.days

# 2. A new island starts when the difference is greater than 1, or it's the first row (NaN)
df["is_new_island"] = (df["date_diff"] > 1) | (df["date_diff"].isna())

# 3. Create an island ID using cumsum (True evaluates to 1, False to 0)
df["island_id"] = df.groupby("user_id")["is_new_island"].cumsum()

# 4. Group by user and island ID to find the start and end of the streak
result = df.groupby(["user_id", "island_id"]).agg(
    streak_start=("active_date", "min"),
    streak_end=("active_date", "max"),
    streak_duration_days=("active_date", "count")
).reset_index().drop(columns=["island_id"])
""",
        "solution_sql": """
-- The Classic ROW_NUMBER() grouping trick
WITH NumberedDates AS (
    SELECT 
        user_id,
        active_date,
        -- Generate sequential numbers (1, 2, 3...)
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY active_date) as rn
    FROM user_activity
),
GroupedIslands AS (
    SELECT 
        user_id,
        active_date,
        -- Subtracting the integers creates a constant 'anchor' date for sequences!
        -- E.g., Jan 2 - 2 days = Dec 31. Jan 3 - 3 days = Dec 31.
        -- Jan 6 - 4 days = Jan 2 (New anchor!)
        CAST(active_date AS DATE) - CAST(rn AS INTEGER) * INTERVAL 1 DAY as island_anchor
    FROM NumberedDates
)
SELECT 
    user_id,
    MIN(active_date) as streak_start,
    MAX(active_date) as streak_end,
    COUNT(active_date) as streak_duration_days
FROM GroupedIslands
GROUP BY user_id, island_anchor
ORDER BY user_id, streak_start;
""",
        "deep_dive": "The Gaps and Islands problem tests advanced window function capability. The SQL 'Row Number subtraction' trick is extremely elegant for sequential integers or standard dates (assuming a daily grain). The Python approach utilizing `diff()` inside a `groupby()` and checking for thresholds before applying a `cumsum()` is highly versatile and works for varying date grains (like seconds) where sequences might be defined by custom time thresholds rather than strict +1 day increments."
    }
