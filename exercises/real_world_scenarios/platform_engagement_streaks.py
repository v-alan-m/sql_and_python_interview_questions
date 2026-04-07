import pandas as pd
import numpy as np

def get_exercise():
    return {
        "title": "Platform Engagement Streaks",
        "subtitle": "Gaps & Islands, Conditional Logic, Cohort Analysis",
        "description": "A streaming platform wants to understand user engagement patterns: 'Can you identify consecutive login streaks, classify users as active/churned/re-engaged, and build a retention cohort table?' This tests window functions, sessionization, and advanced aggregation — core skills for any mid-to-senior DE.",
        "difficulty_level": "mid_to_senior",
        "source_inspiration": "LinkedIn, Netflix, Spotify · DataLemur (User Streaks, Active Users)",
                "data": pd.DataFrame({
                    "user_id": [101, 101, 101, 101, 101, 102, 102, 102, 102],
                    "login_date": [
                        "2024-03-01", "2024-03-02", "2024-03-03", "2024-03-06", "2024-03-07",
                        "2024-03-01", "2024-03-04", "2024-03-05", "2024-03-06"
                    ],
                    "subscription_tier": ["premium"] * 5 + ["basic"] * 4,
                    "signup_date": ["2024-01-15"] * 5 + ["2024-01-10"] * 4
                }),
        "table_name": "user_logins",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "Calculate the day-over-day difference per user with `diff()`. Where the gap is > 1 day (or `NaN` for the first row), a new streak begins. Use `cumsum()` to assign a streak ID, then aggregate to find min/max dates and count.",
        "hint_sql": "Use the `ROW_NUMBER()` trick: subtract the row number (as integer days) from the date. Sequential dates will yield the same 'baseline' date, which can then be used to `GROUP BY`.",
        "solution_python": """\
df["login_date"] = pd.to_datetime(df["login_date"])
df = df.sort_values(["user_id", "login_date"]).reset_index(drop=True)

# 1. Calculate day-over-day diff per user
df["date_diff"] = df.groupby("user_id")["login_date"].diff().dt.days

# 2. New streak starts where gap > 1 or first row (NaN)
df["is_new_streak"] = (df["date_diff"] > 1) | (df["date_diff"].isna())

# 3. Assign streak IDs via cumsum within each user
df["streak_id"] = df.groupby("user_id")["is_new_streak"].cumsum()

# 4. Aggregate to find streak boundaries
result = df.groupby(["user_id", "streak_id"]).agg(
    streak_start=("login_date", "min"),
    streak_end=("login_date", "max"),
    streak_length_days=("login_date", "count")
).reset_index().drop(columns=["streak_id"])
result = result.sort_values(["user_id", "streak_start"]).reset_index(drop=True)""",
        "solution_sql": """\
WITH NumberedLogins AS (
    SELECT
        user_id,
        login_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM user_logins
),
GroupedStreaks AS (
    SELECT
        user_id,
        login_date,
        CAST(login_date AS DATE) - CAST(rn AS INTEGER) * INTERVAL 1 DAY AS streak_anchor
    FROM NumberedLogins
)
SELECT
    user_id,
    MIN(login_date) AS streak_start,
    MAX(login_date) AS streak_end,
    COUNT(*) AS streak_length_days
FROM GroupedStreaks
GROUP BY user_id, streak_anchor
ORDER BY user_id, streak_start;""",
        "deep_dive": "This problem uses the classic 'Gaps and Islands' pattern. Subtracting a sequential `ROW_NUMBER` from a sequential date produces a constant anchor for that continuous streak.",
        "big_o_explanation": "Sorting by user + date dictates O(N log N) time complexity. Using linear difference flags and aggregations operates in O(N). Space complexity is O(N) for partitioning.",
        "mcq_questions": [
            {
                "question": "What is a 'sessionization' problem in data engineering?",
                "stage_number": 1,
                "options": [
                    {"label": "A", "text": "Splitting a database into multiple sessions for performance", "is_correct": False},
                    {"label": "B", "text": "Grouping sequential user events into logical sessions based on time gaps", "is_correct": True},
                    {"label": "C", "text": "Creating user authentication sessions", "is_correct": False},
                    {"label": "D", "text": "Partitioning data by session ID", "is_correct": False}
                ],
                "explanation": "Sessionization groups a stream of timestamped events into logical 'sessions' — e.g., web clicks within 30 minutes of each other. It's a variant of the Gaps & Islands problem. In SQL, you use `LAG()` or `ROW_NUMBER()` subtraction; in Python, `diff()` + `cumsum()` with a threshold. Tools like Google Analytics, Mixpanel, and Amplitude do this."
            },
            {
                "question": "What are DAU, WAU, and MAU and how are they typically computed?",
                "stage_number": 2,
                "options": [
                    {"label": "A", "text": "They are database administration metrics for query optimisation", "is_correct": False},
                    {"label": "B", "text": "Daily/Weekly/Monthly Active Users — distinct user counts within the respective time window", "is_correct": True},
                    {"label": "C", "text": "They measure data throughput in pipelines", "is_correct": False},
                    {"label": "D", "text": "They are computed using SUM() over user login counts", "is_correct": False}
                ],
                "explanation": "**DAU** = distinct users active today. **WAU** = distinct users active in the last 7 days. **MAU** = distinct users active in the last 30 days. Computed via `COUNT(DISTINCT user_id) WHERE login_date BETWEEN ... AND ...`. The ratio **DAU/MAU** (called 'stickiness') is a key product metric."
            },
            {
                "question": "What is a Slowly Changing Dimension (SCD) Type 2?",
                "stage_number": 3,
                "options": [
                    {"label": "A", "text": "A dimension that never changes", "is_correct": False},
                    {"label": "B", "text": "A dimension that overwrites old values with new values", "is_correct": False},
                    {"label": "C", "text": "A dimension that preserves history by creating a new row for each change with effective dates", "is_correct": True},
                    {"label": "D", "text": "A dimension that stores only the latest 2 versions", "is_correct": False}
                ],
                "explanation": "SCD Type 2 tracks full history. Instead of overwriting, you close the old row (`effective_end = today`) and insert a new row (`effective_start = today, effective_end = NULL`). This lets you answer 'What tier was user X on when they made purchase Y?' — critical for accurate historical analysis."
            }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Consecutive Login Streaks",
                "scenario": "The product team wants to surface a 'You're on a streak!' badge to users. Identify each continuous streak of consecutive daily logins per user. Return the user ID, streak start date, streak end date, and streak length in days.",
                "hint": "Calculate the day-over-day difference per user with `diff()`. Where the gap is > 1 day, a new streak begins. Use `cumsum()` to assign a streak ID, then aggregate.",
                "data": pd.DataFrame({
                    "user_id": [101, 101, 101, 101, 101, 102, 102, 102, 102],
                    "login_date": [
                        "2024-03-01", "2024-03-02", "2024-03-03", "2024-03-06", "2024-03-07",
                        "2024-03-01", "2024-03-04", "2024-03-05", "2024-03-06"
                    ],
                    "subscription_tier": ["premium"] * 5 + ["basic"] * 4,
                    "signup_date": ["2024-01-15"] * 5 + ["2024-01-10"] * 4
                }),
                "evaluation_criteria": [
                    "Correctly partitions diff/cumsum by user_id (doesn't blend users together)",
                    "Uses the classic diff() > 1 + cumsum() pattern or SQL ROW_NUMBER() subtraction trick",
                    "Handles single-day streaks (count = 1) as valid streaks"
                ],
                "solution_code": """\
df["login_date"] = pd.to_datetime(df["login_date"])
df = df.sort_values(["user_id", "login_date"]).reset_index(drop=True)

# 1. Calculate day-over-day diff per user
df["date_diff"] = df.groupby("user_id")["login_date"].diff().dt.days

# 2. New streak starts where gap > 1 or first row (NaN)
df["is_new_streak"] = (df["date_diff"] > 1) | (df["date_diff"].isna())

# 3. Assign streak IDs via cumsum within each user
df["streak_id"] = df.groupby("user_id")["is_new_streak"].cumsum()

# 4. Aggregate to find streak boundaries
result = df.groupby(["user_id", "streak_id"]).agg(
    streak_start=("login_date", "min"),
    streak_end=("login_date", "max"),
    streak_length_days=("login_date", "count")
).reset_index().drop(columns=["streak_id"])
result = result.sort_values(["user_id", "streak_start"]).reset_index(drop=True)""",
                "solution_sql": """\
WITH NumberedLogins AS (
    SELECT
        user_id,
        login_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM user_logins
),
GroupedStreaks AS (
    SELECT
        user_id,
        login_date,
        CAST(login_date AS DATE) - CAST(rn AS INTEGER) * INTERVAL 1 DAY AS streak_anchor
    FROM NumberedLogins
)
SELECT
    user_id,
    MIN(login_date) AS streak_start,
    MAX(login_date) AS streak_end,
    COUNT(*) AS streak_length_days
FROM GroupedStreaks
GROUP BY user_id, streak_anchor
ORDER BY user_id, streak_start;""",
                "expected_output": pd.DataFrame({
                    "user_id": [101, 101, 102, 102],
                    "streak_start": pd.to_datetime(["2024-03-01", "2024-03-06", "2024-03-01", "2024-03-04"]),
                    "streak_end": pd.to_datetime(["2024-03-03", "2024-03-07", "2024-03-01", "2024-03-06"]),
                    "streak_length_days": [3, 2, 1, 3]
                }),
                "big_o_explanation": "Time: O(N log N) due to sorting by user + date. Space: O(N) for intermediate diff flags and grouping attributes.",
                "follow_up_probes": [
                    "What if the platform logged logins at the hour/minute level instead of daily? How would you adapt the threshold?",
                    "Explain exactly how subtracting ROW_NUMBER() from a sequential date produces a constant anchor value."
                ]
            },
            {
                "stage_number": 2,
                "title": "User Status Classification",
                "scenario": "The leadership team wants a quick snapshot of user health. Using a reference date of `2024-03-10`, classify each user based on their most recent login: 'active' (<= 7 days ago), 'at_risk' (8–29 days ago), or 'churned' (30+ days ago).",
                "hint": "Find each user's most recent login date via `groupby().max()`. Then compute the number of days since the reference date and apply conditional logic (`np.select()` or `CASE WHEN`).",
                "data": pd.DataFrame({
                    "user_id": [101, 101, 102, 102, 103, 104, 105],
                    "login_date": [
                        "2024-03-09", "2024-03-05", "2024-02-20", "2024-02-15",
                        "2024-01-05", "2024-03-08", "2024-02-25"
                    ],
                    "subscription_tier": ["premium", "premium", "basic", "basic", "free", "free", "premium"],
                    "signup_date": ["2024-01-15", "2024-01-15", "2024-01-10", "2024-01-10", "2023-11-01", "2024-02-01", "2024-01-20"]
                }),
                "evaluation_criteria": [
                    "Correctly identifies that MAX(login_date) gives the most recent login",
                    "Uses ordered conditional logic (checks <= 7 before <= 29) to avoid misclassification"
                ],
                "solution_code": """\
import numpy as np

df["login_date"] = pd.to_datetime(df["login_date"])
reference_date = pd.to_datetime("2024-03-10")

# 1. Find each user's most recent login
last_login = df.groupby("user_id", as_index=False)["login_date"].max()
last_login = last_login.rename(columns={"login_date": "last_login"})

# 2. Calculate days since last login
last_login["days_since_login"] = (reference_date - last_login["last_login"]).dt.days

# 3. Classify users
conditions = [
    last_login["days_since_login"] <= 7,
    last_login["days_since_login"] <= 29,
]
choices = ["active", "at_risk"]
last_login["user_status"] = np.select(conditions, choices, default="churned")

result = last_login[["user_id", "last_login", "days_since_login", "user_status"]]
result = result.sort_values("user_id").reset_index(drop=True)""",
                "solution_sql": """\
WITH LastLogin AS (
    SELECT
        user_id,
        MAX(CAST(login_date AS DATE)) AS last_login
    FROM user_logins
    GROUP BY user_id
)
SELECT
    user_id,
    last_login,
    DATEDIFF('day', last_login, CAST('2024-03-10' AS DATE)) AS days_since_login,
    CASE
        WHEN DATEDIFF('day', last_login, CAST('2024-03-10' AS DATE)) <= 7 THEN 'active'
        WHEN DATEDIFF('day', last_login, CAST('2024-03-10' AS DATE)) <= 29 THEN 'at_risk'
        ELSE 'churned'
    END AS user_status
FROM LastLogin
ORDER BY user_id;""",
                "expected_output": pd.DataFrame({
                    "user_id": [101, 102, 103, 104, 105],
                    "last_login": pd.to_datetime(["2024-03-09", "2024-02-20", "2024-01-05", "2024-03-08", "2024-02-25"]),
                    "days_since_login": [1, 19, 65, 2, 14],
                    "user_status": ["active", "at_risk", "churned", "active", "at_risk"]
                }),
                "big_o_explanation": "Time: O(N) to iterate and find max login per user, then O(U) for applying the status condition where U is unique users. Space is O(U).",
                "follow_up_probes": [
                    "How would you parameterize the reference date so this runs as a daily batch job?",
                    "What's the difference between np.select() and np.where() for multi-condition classification?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Monthly Retention Cohort Table",
                "scenario": "The executive team wants a retention cohort table: for each signup month, what percentage of users are still active in month+1, month+2, month+3, etc.? Build a cohort table where rows = signup month, columns = months since signup, values = retention rate (%).",
                "hint": "Compute each user's signup month and each login's activity month. Calculate months_since_signup. Use pivot_table to reshape. In SQL, use conditional aggregation and join the month-0 cohort sizes.",
                "data": pd.DataFrame({
                    "user_id": [1, 1, 1, 1, 2, 2, 3, 3, 3, 4, 5],
                    "login_date": [
                        "2024-01-05", "2024-01-15", "2024-02-10", "2024-03-20",
                        "2024-01-10", "2024-02-05", 
                        "2024-02-01", "2024-02-15", "2024-03-10",
                        "2024-02-20", "2024-01-08"
                    ],
                    "subscription_tier": ["free"]*4 + ["basic"]*2 + ["premium"]*3 + ["free", "basic"],
                    "signup_date": ["2024-01-01"]*4 + ["2024-01-01"]*2 + ["2024-02-01"]*3 + ["2024-02-01", "2024-01-01"]
                }),
                "evaluation_criteria": [
                    "Correctly derives cohort_month from signup_date and maps logins to activity_month",
                    "Uses nunique() / COUNT(DISTINCT) since a user may log in multiple times per month",
                    "Computes retention percentage using the month 0 cohort size base."
                ],
                "solution_code": """\
df["login_date"] = pd.to_datetime(df["login_date"])
df["signup_date"] = pd.to_datetime(df["signup_date"])

# 1. Compute cohort month (signup month) and activity month
df["cohort_month"] = df["signup_date"].dt.to_period("M")
df["activity_month"] = df["login_date"].dt.to_period("M")

# 2. Calculate months since signup
df["months_since_signup"] = (df["activity_month"] - df["cohort_month"]).apply(lambda x: x.n)

# 3. Distinct users per cohort per period
cohort_activity = df.groupby(["cohort_month", "months_since_signup"])["user_id"].nunique().reset_index()
cohort_activity = cohort_activity.rename(columns={"user_id": "active_users"})

# 4. Total users per cohort (month 0 count)
cohort_sizes = cohort_activity[cohort_activity["months_since_signup"] == 0][["cohort_month", "active_users"]]
cohort_sizes = cohort_sizes.rename(columns={"active_users": "cohort_size"})

# 5. Merge and compute retention rate
cohort_activity = cohort_activity.merge(cohort_sizes, on="cohort_month")
cohort_activity["retention_rate"] = (
    (cohort_activity["active_users"] / cohort_activity["cohort_size"]) * 100
).round(1)

# 6. Pivot to cohort table format
result = cohort_activity.pivot_table(
    index="cohort_month",
    columns="months_since_signup",
    values="retention_rate"
).reset_index()
result.columns = ["cohort_month"] + [f"month_{int(c)}" for c in result.columns[1:]]
result["cohort_month"] = result["cohort_month"].astype(str)
result = result.reset_index(drop=True)""",
                "solution_sql": """\
WITH CohortData AS (
    SELECT
        user_id,
        CAST(signup_date AS DATE) AS signup_date,
        CAST(login_date AS DATE) AS login_date
    FROM user_logins
),
MonthsSince AS (
    SELECT
        SUBSTRING(CAST(signup_date AS VARCHAR), 1, 7) AS cohort_month,
        CAST((EXTRACT(YEAR FROM login_date) - EXTRACT(YEAR FROM signup_date)) * 12 +
        (EXTRACT(MONTH FROM login_date) - EXTRACT(MONTH FROM signup_date)) AS INTEGER) AS months_since_signup,
        COUNT(DISTINCT user_id) AS active_users
    FROM CohortData
    GROUP BY cohort_month, months_since_signup
),
CohortSizes AS (
    SELECT cohort_month, active_users AS cohort_size
    FROM MonthsSince
    WHERE months_since_signup = 0
)
SELECT
    ms.cohort_month,
    MAX(CASE WHEN ms.months_since_signup = 0 THEN ROUND(ms.active_users * 100.0 / cs.cohort_size, 1) END) AS month_0,
    MAX(CASE WHEN ms.months_since_signup = 1 THEN ROUND(ms.active_users * 100.0 / cs.cohort_size, 1) END) AS month_1,
    MAX(CASE WHEN ms.months_since_signup = 2 THEN ROUND(ms.active_users * 100.0 / cs.cohort_size, 1) END) AS month_2
FROM MonthsSince ms
JOIN CohortSizes cs ON ms.cohort_month = cs.cohort_month
GROUP BY ms.cohort_month
ORDER BY ms.cohort_month;""",
                "expected_output": pd.DataFrame({
                    "cohort_month": ["2024-01", "2024-02"],
                    "month_0": [100.0, 100.0],
                    "month_1": [66.7, 50.0],
                    "month_2": [33.3, np.nan]
                }),
                "big_o_explanation": "Time: O(N) for cohort assignment + O(N) for groupby + O(C * M) for the pivot where C=cohorts and M=month periods. Space is O(C * M) for the pivoted table.",
                "follow_up_probes": [
                    "Why do we use nunique() rather than count() for active users?",
                    "How would you extend this to a weekly retention cohort instead of monthly?"
                ]
            }
        ]
    }
