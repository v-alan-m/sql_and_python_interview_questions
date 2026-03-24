# Scenario 3: Platform Engagement — Gaps & Islands

**Source Inspiration:** LinkedIn, Netflix, Spotify · DataLemur (User Streaks, Active Users)
**Level Range:** Mid → Senior
**Description:** A streaming platform wants to understand user engagement patterns: "Can you identify consecutive login streaks, classify users as active/churned/re-engaged, and build a retention cohort table?" This tests window functions, sessionization, and advanced aggregation — core skills for any mid-to-senior DE.

## Data Schema (`user_logins`)
| Column | Type | Description |
|--------|------|-------------|
| user_id | int | Unique user identifier |
| login_date | str (date) | Date of login activity |
| subscription_tier | str | "free", "basic", "premium" |
| signup_date | str (date) | Original signup date (for cohort analysis) |

---
## Stages

### Stage 1: Consecutive Login Streaks
**Level:** Mid
**Key Concepts:** Gaps & Islands: `diff()` + `cumsum()`, `ROW_NUMBER()` subtraction
**Scenario:** The product team wants to surface a "You're on a 7-day streak!" badge to users. To power this feature, identify each continuous streak of consecutive daily logins per user. Return the user ID, streak start date, streak end date, and streak length in days.
**Coding Task:** Find start/end of each continuous login streak per user.

**Hint:** Calculate the day-over-day difference per user with `diff()`. Where the gap is > 1 day (or `NaN` for the first row), a new streak begins. Use `cumsum()` to assign a streak ID, then aggregate to find min/max dates and count.

**Sample Data:**
```
user_id | login_date
101     | 2024-03-01
101     | 2024-03-02
101     | 2024-03-03
101     | 2024-03-06
101     | 2024-03-07
102     | 2024-03-01
102     | 2024-03-04
102     | 2024-03-05
102     | 2024-03-06
```

**Python Solution:**
```python
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
result = result.sort_values(["user_id", "streak_start"]).reset_index(drop=True)
```

**SQL Solution:**
```sql
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
ORDER BY user_id, streak_start;
```

**Expected Output Data Shape:** `user_id`, `streak_start`, `streak_end`, `streak_length_days`
- user 101: streak 1 (Mar 1–3, 3 days), streak 2 (Mar 6–7, 2 days)
- user 102: streak 1 (Mar 1, 1 day), streak 2 (Mar 4–6, 3 days)

**Big-O Analysis:**
- **Time:** O(N log N) — sorting by user + date dominates; diff/cumsum/aggregation are O(N)
- **Space:** O(N) for intermediate diff flags, streak IDs, and grouped output

**Evaluation Criteria:**
- Correctly partitions diff/cumsum by `user_id` (doesn't blend users together)
- Uses the classic `diff() > 1` + `cumsum()` pattern (Python) or `ROW_NUMBER()` subtraction trick (SQL)
- Handles single-day streaks (count = 1) as valid streaks

**Follow-Up Probes:**
- "What if the platform logged logins at the hour/minute level instead of daily? How would you adapt the threshold?"
- "Explain exactly how subtracting `ROW_NUMBER()` from a sequential date produces a constant anchor value."
- "Would `DENSE_RANK()` work here instead of `ROW_NUMBER()`? What are the trade-offs?"

---
### Stage 2: User Status Classification
**Level:** Mid
**Key Concepts:** Conditional logic on date diffs, `CASE WHEN`, `np.select()`
**Scenario:** The leadership team wants a quick snapshot of user health. Using a reference date of `2024-03-10`, classify each user based on their most recent login: **"active"** if they logged in within the last 7 days, **"at_risk"** if their last login was 8–29 days ago, or **"churned"** if 30+ days since their last login.
**Coding Task:** Label each user as "active", "at_risk", or "churned" based on recency from a reference date.

**Hint:** Find each user's most recent login date via `groupby().max()`. Then compute the number of days since the reference date and apply conditional logic.

**Sample Data:**
```
user_id | login_date       | subscription_tier | signup_date
101     | 2024-03-09       | premium           | 2024-01-15
101     | 2024-03-05       | premium           | 2024-01-15
102     | 2024-02-20       | basic             | 2024-01-10
102     | 2024-02-15       | basic             | 2024-01-10
103     | 2024-01-05       | free              | 2023-11-01
104     | 2024-03-08       | free              | 2024-02-01
105     | 2024-02-25       | premium           | 2024-01-20
```

**Python Solution:**
```python
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
result = result.sort_values("user_id").reset_index(drop=True)
```

**SQL Solution:**
```sql
WITH LastLogin AS (
    SELECT
        user_id,
        MAX(login_date) AS last_login
    FROM user_logins
    GROUP BY user_id
)
SELECT
    user_id,
    last_login,
    DATEDIFF('day', last_login, '2024-03-10') AS days_since_login,
    CASE
        WHEN DATEDIFF('day', last_login, '2024-03-10') <= 7 THEN 'active'
        WHEN DATEDIFF('day', last_login, '2024-03-10') <= 29 THEN 'at_risk'
        ELSE 'churned'
    END AS user_status
FROM LastLogin
ORDER BY user_id;
```

**Expected Output Data Shape:** `user_id`, `last_login`, `days_since_login`, `user_status`
- 101 → last login Mar 9, 1 day ago → "active"
- 102 → last login Feb 20, 19 days ago → "at_risk"
- 103 → last login Jan 5, 65 days ago → "churned"
- 104 → last login Mar 8, 2 days ago → "active"
- 105 → last login Feb 25, 14 days ago → "at_risk"

**Big-O Analysis:**
- **Time:** O(N) — single pass to find max login per user, then O(U) for classification where U = distinct users
- **Space:** O(U) for the aggregated user-level result

**Evaluation Criteria:**
- Correctly identifies that `MAX(login_date)` gives the most recent login
- Uses ordered conditional logic (checks ≤ 7 before ≤ 29) to avoid misclassification
- Understands the business meaning of each status bucket and chooses appropriate thresholds

**Follow-Up Probes:**
- "How would you parameterize the reference date so this runs as a daily batch job?"
- "If a user re-activates after churning, should their status change? How would you track re-engagement?"
- "What's the difference between `np.select()` and `np.where()` for multi-condition classification?"

---
### Stage 3: Monthly Retention Cohort Table
**Level:** Senior
**Key Concepts:** Cohort analysis, CROSS JOIN with month series, conditional aggregation, `pivot_table()`
**Scenario:** The executive team wants a **retention cohort table**: for each signup month, what percentage of users are still active in month+1, month+2, month+3, etc.? This is the gold-standard retention metric used by companies like Netflix, Spotify, and Facebook.
**Coding Task:** Build a cohort table where rows = signup month, columns = months since signup, values = retention rate (%).

**Hint:** In Python, compute each user's signup month and each login's activity month, then calculate months_since_signup. Use `pivot_table` to reshape. In SQL, generate a month series with a CROSS JOIN and use conditional aggregation.

**Sample Data:**
```
user_id | login_date | subscription_tier | signup_date
1       | 2024-01-05 | free              | 2024-01-01
1       | 2024-01-15 | free              | 2024-01-01
1       | 2024-02-10 | free              | 2024-01-01
1       | 2024-03-20 | free              | 2024-01-01
2       | 2024-01-10 | basic             | 2024-01-01
2       | 2024-02-05 | basic             | 2024-01-01
3       | 2024-02-01 | premium           | 2024-02-01
3       | 2024-02-15 | premium           | 2024-02-01
3       | 2024-03-10 | premium           | 2024-02-01
4       | 2024-02-20 | free              | 2024-02-01
5       | 2024-01-08 | basic             | 2024-01-01
```

**Python Solution:**
```python
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
result = result.reset_index(drop=True)
```

**SQL Solution:**
```sql
WITH CohortData AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month,
        DATE_TRUNC('month', login_date) AS activity_month
    FROM user_logins
),
MonthsSince AS (
    SELECT
        cohort_month,
        DATEDIFF('month', cohort_month, activity_month) AS months_since_signup,
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
    ms.months_since_signup,
    ms.active_users,
    cs.cohort_size,
    ROUND(ms.active_users * 100.0 / cs.cohort_size, 1) AS retention_rate
FROM MonthsSince ms
JOIN CohortSizes cs ON ms.cohort_month = cs.cohort_month
ORDER BY ms.cohort_month, ms.months_since_signup;
```

**Expected Output Data Shape:** Pivoted table with `cohort_month`, `month_0`, `month_1`, `month_2`
- Cohort 2024-01 (3 users): month_0 = 100.0%, month_1 = 66.7% (users 1 & 2 active in Feb), month_2 = 33.3% (only user 1 in Mar)
- Cohort 2024-02 (2 users): month_0 = 100.0%, month_1 = 50.0% (only user 3 in Mar)

**Big-O Analysis:**
- **Time:** O(N) for cohort assignment + O(N) for groupby + O(C × M) for the pivot where C = cohorts and M = month periods
- **Space:** O(C × M) for the output cohort table; O(N) for intermediate grouped data

**Evaluation Criteria:**
- Correctly derives `cohort_month` from `signup_date` and maps logins to `activity_month`
- Uses `nunique()` / `COUNT(DISTINCT)` — not `count()` — since a user may log in multiple times per month
- Computes retention as `active_users / cohort_size * 100`, where cohort_size = count at month_0
- Understands the business significance: retention curves that flatten indicate product-market fit

**Follow-Up Probes:**
- "Why do we use `nunique()` rather than `count()` for active users?"
- "How would you extend this to a weekly retention cohort instead of monthly?"
- "What does a concave vs convex retention curve tell you about the product?"
- "How would you handle users who signed up and never logged in (they should appear in month_0 but with 0 activity)?"

---
## MCQ Bank

**Q1 (Stage 1):** *"What is a 'sessionization' problem in data engineering?"*
- A) Splitting a database into multiple sessions for performance (Incorrect)
- B) Grouping sequential user events into logical sessions based on time gaps (Correct)
- C) Creating user authentication sessions (Incorrect)
- D) Partitioning data by session ID (Incorrect)
- **Explanation:** Sessionization groups a stream of timestamped events into logical "sessions" — e.g., web clicks within 30 minutes of each other belong to the same session. It's a variant of the Gaps & Islands problem. In SQL, you use `LAG()` or `ROW_NUMBER()` subtraction; in Python, `diff()` + `cumsum()` with a threshold. Google Analytics, Mixpanel, and Amplitude all do this under the hood.

**Q2 (Stage 2):** *"What are DAU, WAU, and MAU and how are they typically computed?"*
- A) They are database administration metrics for query optimisation (Incorrect)
- B) Daily/Weekly/Monthly Active Users — distinct user counts within the respective time window (Correct)
- C) They measure data throughput in pipelines (Incorrect)
- D) They are computed using SUM() over user login counts (Incorrect)
- **Explanation:** **DAU** = distinct users active today. **WAU** = distinct users active in the last 7 days. **MAU** = distinct users active in the last 30 days. Computed via `COUNT(DISTINCT user_id) WHERE login_date BETWEEN ... AND ...`. The ratio **DAU/MAU** (called "stickiness") is a key product metric — Facebook/Meta famously targets >50%.

**Q3 (Stage 3):** *"What is a Slowly Changing Dimension (SCD) Type 2?"*
- A) A dimension that never changes (Incorrect)
- B) A dimension that overwrites old values with new values (Incorrect)
- C) A dimension that preserves history by creating a new row for each change with effective dates (Correct)
- D) A dimension that stores only the latest 2 versions (Incorrect)
- **Explanation:** SCD Type 2 tracks full history. When a user changes subscription from "free" to "premium", instead of overwriting, you close the old row (`effective_end = today`) and insert a new row (`effective_start = today, effective_end = NULL`). This lets you answer "What tier was user X on when they made purchase Y?" — critical for accurate historical analysis. Type 1 = overwrite (no history), Type 3 = add a "previous_value" column (limited history).
