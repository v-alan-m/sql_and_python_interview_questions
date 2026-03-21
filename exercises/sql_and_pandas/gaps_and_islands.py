import pandas as pd

def get_exercise():
    return {
        "title": "Gaps and Islands",
        "subtitle": "Window Functions, GROUP BY, Common Table Expressions (CTEs), Pandas Aggregation",
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
        "deep_dive": "The Gaps and Islands problem tests advanced window function capability. The SQL 'Row Number subtraction' trick is extremely elegant for sequential integers or standard dates (assuming a daily grain). The Python approach utilizing `diff()` inside a `groupby()` and checking for thresholds before applying a `cumsum()` is highly versatile and works for varying date grains (like seconds) where sequences might be defined by custom time thresholds rather than strict +1 day increments.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Identify Consecutive Dates (Single User)",
                "scenario": "Given a sorted list of active dates for a *single user*, identify continuous streaks of activity. Return the `user_id`, start date, end date, and duration in days for each continuous streak.",
                "hint": "Calculate the difference in days between the current and previous date. Differences > 1 day indicate the start of a new streak.",
                "data": pd.DataFrame({
                    "user_id": [1, 1, 1, 1, 1],
                    "active_date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-06", "2023-01-07"]
                }),
                "evaluation_criteria": [
                    "Understanding of how to isolate continuous sequences using difference calculations or window functions.",
                    "Ability to generate a cumulative grouping ID for sequences.",
                    "Basic aggregation logic to extract min, max, and count."
                ],
                "solution_code": """\
df["active_date"] = pd.to_datetime(df["active_date"])

# 1. Calculate difference between current date and previous date
df["date_diff"] = df["active_date"].diff().dt.days

# 2. A new island starts when difference > 1, or it's the first row
df["is_new_island"] = (df["date_diff"] > 1) | (df["date_diff"].isna())

# 3. Create an island ID using cumsum
df["island_id"] = df["is_new_island"].cumsum()

# 4. Group by user and island ID to find streak properties
result = df.groupby(["user_id", "island_id"]).agg(
    streak_start=("active_date", "min"),
    streak_end=("active_date", "max"),
    streak_duration_days=("active_date", "count")
).reset_index().drop(columns=["island_id"])""",
                "solution_sql": """\
WITH NumberedDates AS (
    SELECT 
        user_id,
        active_date,
        ROW_NUMBER() OVER (ORDER BY active_date) as rn
    FROM user_activity
),
GroupedIslands AS (
    SELECT 
        user_id,
        active_date,
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
ORDER BY streak_start;""",
                "expected_output": pd.DataFrame({
                    "user_id": [1, 1],
                    "streak_start": pd.to_datetime(["2023-01-01", "2023-01-06"]),
                    "streak_end": pd.to_datetime(["2023-01-03", "2023-01-07"]),
                    "streak_duration_days": [3, 2]
                }),
                "follow_up_probes": [
                    "What if the differences were calculated in hours instead of days? How would your threshold logic change?",
                    "Explain exactly how subtracting an auto-incrementing ROW_NUMBER from a sequential date outputs a constant value."
                ]
            },
            {
                "stage_number": 2,
                "title": "Multiple Users",
                "scenario": "The platform has grown! Now the data contains activity for *multiple users*. Modify your logic to find the streaks independently for each user.",
                "hint": "A naive diff() or cumsum() across the entire dataframe will blend users together. Group by user_id before applying these operations.",
                "data": pd.DataFrame({
                    "user_id": [1, 1, 1, 1, 1, 2, 2, 2],
                    "active_date": [
                        "2023-01-01", "2023-01-02", "2023-01-03", 
                        "2023-01-06", "2023-01-07", 
                        "2023-01-01", "2023-01-03", "2023-01-04"
                    ]
                }),
                "evaluation_criteria": [
                    "Correct use of independent grouping scopes for operations that track 'previous state' (like diffs).",
                    "Translating cross-sectional operations into partitioned ones."
                ],
                "solution_code": """\
df["active_date"] = pd.to_datetime(df["active_date"])

# 1. Group by user before calculating diff
df["date_diff"] = df.groupby("user_id")["active_date"].diff().dt.days

# 2. Island flag
df["is_new_island"] = (df["date_diff"] > 1) | (df["date_diff"].isna())

# 3. Group by user before cumsum
df["island_id"] = df.groupby("user_id")["is_new_island"].cumsum()

# 4. Group by user and island ID
result = df.groupby(["user_id", "island_id"]).agg(
    streak_start=("active_date", "min"),
    streak_end=("active_date", "max"),
    streak_duration_days=("active_date", "count")
).reset_index().drop(columns=["island_id"])""",
                "solution_sql": """\
WITH NumberedDates AS (
    SELECT 
        user_id,
        active_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY active_date) as rn
    FROM user_activity
),
GroupedIslands AS (
    SELECT 
        user_id,
        active_date,
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
ORDER BY user_id, streak_start;""",
                "expected_output": pd.DataFrame({
                    "user_id": [1, 1, 2, 2],
                    "streak_start": pd.to_datetime(["2023-01-01", "2023-01-06", "2023-01-01", "2023-01-03"]),
                    "streak_end": pd.to_datetime(["2023-01-03", "2023-01-07", "2023-01-01", "2023-01-04"]),
                    "streak_duration_days": [3, 2, 1, 2]
                }),
                "follow_up_probes": [
                    "What if a user only logs in once and never again? How does your code represent a '1-day streak'?",
                    "In Python, how do groupby().diff() and groupby().cumsum() scale with millions of users?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Out-of-Order Dates and Duplicates",
                "scenario": "Upstream systems sometimes emit duplicate logs, and events can arrive out of order. Before building islands, you must ensure the data is properly deduplicated and sorted.",
                "hint": "Use drop_duplicates() and sort_values() before any difference calculations, or SELECT DISTINCT in a SQL CTE.",
                "data": pd.DataFrame({
                    "user_id": [2, 1, 1, 2, 1, 2, 1, 1, 2, 1],
                    "active_date": [
                        "2023-01-03", "2023-01-03", "2023-01-01", 
                        "2023-01-04", "2023-01-02", "2023-01-01", 
                        "2023-01-06", "2023-01-07", "2023-01-03",
                        "2023-01-01"
                    ]
                }),
                "evaluation_criteria": [
                    "Defensive engineering: never trusting chronological data to arrive perfectly sorted or unique.",
                    "Understanding of CTE architecture in SQL to prepare standard datasets before window function execution."
                ],
                "solution_code": """\
df["active_date"] = pd.to_datetime(df["active_date"])

# 0. Deduplicate and order dates
df = df.drop_duplicates(subset=["user_id", "active_date"])
df = df.sort_values(by=["user_id", "active_date"])

# 1. Group by user before calculating diff
df["date_diff"] = df.groupby("user_id")["active_date"].diff().dt.days

# 2. Island flag
df["is_new_island"] = (df["date_diff"] > 1) | (df["date_diff"].isna())

# 3. Group by user before cumsum
df["island_id"] = df.groupby("user_id")["is_new_island"].cumsum()

# 4. Group by user and island ID
result = df.groupby(["user_id", "island_id"]).agg(
    streak_start=("active_date", "min"),
    streak_end=("active_date", "max"),
    streak_duration_days=("active_date", "count")
).reset_index().drop(columns=["island_id"])""",
                "solution_sql": """\
WITH DistinctActivity AS (
    SELECT DISTINCT user_id, active_date
    FROM user_activity
),
NumberedDates AS (
    SELECT 
        user_id,
        active_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY active_date) as rn
    FROM DistinctActivity
),
GroupedIslands AS (
    SELECT 
        user_id,
        active_date,
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
ORDER BY user_id, streak_start;""",
                "expected_output": pd.DataFrame({
                    "user_id": [1, 1, 2, 2],
                    "streak_start": pd.to_datetime(["2023-01-01", "2023-01-06", "2023-01-01", "2023-01-03"]),
                    "streak_end": pd.to_datetime(["2023-01-03", "2023-01-07", "2023-01-01", "2023-01-04"]),
                    "streak_duration_days": [3, 2, 1, 2]
                }),
                "follow_up_probes": [
                    "In SQL, if we didn't deduplicate first with DISTINCT, could we have used DENSE_RANK() instead of ROW_NUMBER()? What would be the trade-off or risk on the final COUNT() aggregation?"
                ]
            }
        ]
    }
