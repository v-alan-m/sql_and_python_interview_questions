import pandas as pd

def get_exercise():
    return {
        "title": "Remove Duplicates",
        "subtitle": "Window Functions, GROUP BY, Common Table Expressions (CTEs), Pandas Aggregation",
        "description": "Given a dataset of users, some users appear multiple times with different email addresses. Keep only the row with the most recently updated email address for each user_id. Remove the duplicate user rows.",
        "data": pd.DataFrame({
            "user_id": [101, 101, 102, 103, 101, 102],
            "email": ["old@a.com", "new@a.com", "b@b.com", "c@c.com", "fail@a.com", "new_b@b.com"],
            "updated_at": [
                "2023-01-01", "2023-02-15", "2023-01-10", 
                "2023-03-01", "2022-12-01", "2023-04-20"
            ]
        }),
        "table_name": "user_records",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "Sort the DataFrame by 'user_id' and 'updated_at' (descending). Then use the DataFrame `.drop_duplicates()` method, specifying a subset constraint on 'user_id' and keeping the 'first' instance.",
        "hint_sql": "Use the `ROW_NUMBER()` window function. Partition by 'user_id' and order by 'updated_at' descending. Then, filter where the row number equals 1. You will need a CTE or subquery.",
        "solution_python": """
df["updated_at"] = pd.to_datetime(df["updated_at"])

# Sort by user_id and then chronologically descending
df = df.sort_values(by=["user_id", "updated_at"], ascending=[True, False])

# Drop duplicates keeping the highest chronological value
result = df.drop_duplicates(subset=["user_id"], keep="first").reset_index(drop=True)
""",
        "solution_sql": """
WITH RankedUsers AS (
    SELECT 
        user_id,
        email,
        updated_at,
        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY updated_at DESC) as rn
    FROM user_records
)
SELECT 
    user_id,
    email,
    updated_at
FROM RankedUsers
WHERE rn = 1;
""",
        "deep_dive": "The Python `drop_duplicates` backed by sorting is highly readable. The sort dictates the O(N log N) performance hit. In SQL, the `ROW_NUMBER()` function allows us to maintain the entire row's context (like the email) while aggregating based on another column (`updated_at`). Using a simple `GROUP BY` and `MAX(updated_at)` makes it hard to fetch the correct corresponding email if multiple emails exist per user, which is why window functions are superior for contextual deduplication.",
        "big_o_explanation": "Time Complexity: O(N log N) in Python due to `.sort_values()` across the entire dataframe. In SQL, `ROW_NUMBER() OVER(PARTITION BY ... ORDER BY ...)` also inherently relies on a sorting operation under the hood, making it O(N log N) within each partition. Space Complexity: O(N) to hold the DataFrames and window partitions context in memory. The optimization here is replacing self-joins or nested queries with window functions/sorts, extracting the exact row context chronologically without Cartesian product explosions.",
        
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Latest Update Date per User",
                "scenario": "Before we retrieve the full user record, let's start simple. Can you return each `user_id` and their most recent `updated_at` date? We do not need the email yet.",
                "hint": "In Python, group by `user_id` and find the maximum of the `updated_at` column. In SQL, use a basic `GROUP BY`.",
                "data": pd.DataFrame({
                    "user_id": [101, 101, 102, 103, 101],
                    "email": ["old@a.com", "new@a.com", "b@b.com", "c@c.com", "fail@a.com"],
                    "updated_at": ["2023-01-01", "2023-02-15", "2023-01-10", "2023-03-01", "2022-12-01"]
                }),
                "evaluation_criteria": [
                    "Understands basic aggregation logic",
                    "Can correctly implement `groupby` + `max()` in Pandas or `MAX()` with `GROUP BY` in SQL"
                ],
                "solution_code": """\\
df["updated_at"] = pd.to_datetime(df["updated_at"])
result = df.groupby("user_id")["updated_at"].max().reset_index()
""",
                "solution_sql": """
SELECT 
    user_id, 
    MAX(updated_at) as updated_at
FROM user_records
GROUP BY user_id
ORDER BY user_id;
""",
                "expected_output": pd.DataFrame({
                    "user_id": [101, 102, 103],
                    "updated_at": pd.to_datetime(["2023-02-15", "2023-01-10", "2023-03-01"])
                }),
                "big_o_explanation": "Time Complexity: O(N) in python `groupby(...).max()` and SQL `GROUP BY`. Aggregation functions perform a single pass over the dataset hashing and tracking the running maximum. Space Complexity: O(U) where U is the number of unique users for the output. Because we don't need the corresponding 'email' context column, avoiding a full table sort yields massive performance benefits.",
                "follow_up_probes": [
                    "What happens if a user has no records in the table? (Trick question: they wouldn't be grouped)",
                    "Is it guaranteed that the resulting records are sorted by user_id?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Full Record of Latest Update",
                "scenario": "Great. Now the product team actually needs the specific email address associated with that most recent update. Return the full row (`user_id`, `email`, `updated_at`) for the latest update per user.",
                "hint": "A simple `GROUP BY` won't work easily here to fetch the `email`. In Python, try sorting and dropping duplicates. In SQL, you will need a window function like `ROW_NUMBER()`.",
                "data": pd.DataFrame({
                    "user_id": [101, 101, 102, 103, 101, 102],
                    "email": ["old@a.com", "new@a.com", "b@b.com", "c@c.com", "fail@a.com", "new_b@b.com"],
                    "updated_at": [
                        "2023-01-01", "2023-02-15", "2023-01-10", 
                        "2023-03-01", "2022-12-01", "2023-04-20"
                    ]
                }),
                "evaluation_criteria": [
                    "Identifies that `GROUP BY` is insufficient for retrieving parallel context columns",
                    "Can implement `ROW_NUMBER()` in SQL",
                    "Understands how `.sort_values()` combined with `.drop_duplicates()` achieves contextual deduplication in Python"
                ],
                "solution_code": """\\
df["updated_at"] = pd.to_datetime(df["updated_at"])
df = df.sort_values(by=["user_id", "updated_at"], ascending=[True, False])
result = df.drop_duplicates(subset=["user_id"], keep="first").reset_index(drop=True)
""",
                "solution_sql": """
WITH RankedUsers AS (
    SELECT 
        user_id,
        email,
        updated_at,
        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY updated_at DESC) as rn
    FROM user_records
)
SELECT 
    user_id,
    email,
    updated_at
FROM RankedUsers
WHERE rn = 1
ORDER BY user_id;
""",
                "expected_output": pd.DataFrame({
                    "user_id": [101, 102, 103],
                    "email": ["new@a.com", "new_b@b.com", "c@c.com"],
                    "updated_at": pd.to_datetime(["2023-02-15", "2023-04-20", "2023-03-01"])
                }),
                "big_o_explanation": "Time Complexity: O(N log N). Whether using Python's `.sort_values()` or SQL's `ROW_NUMBER() OVER(ORDER BY ...)`, the engine must sort records before deduplication. Space Complexity: O(N) to hold the sorted dataset temporarily in memory. Keeping contextual columns forces us away from linear `GROUP BY` aggregations and into O(N log N) sorts, but it avoids O(N^2) naive subquery looping.",
                "follow_up_probes": [
                    "Why did you use `ROW_NUMBER()` instead of `RANK()` or `DENSE_RANK()`?",
                    "What is the time complexity of the sorting operation in Python?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Tie-Breaking Same-Day Updates",
                "scenario": "Sometimes our system registers two email updates on the exact same date for the same user. To ensure deterministic results, if a user has multiple updates on their most recent date, return the row with the email address that comes *last* alphabetically.",
                "hint": "You need to add a secondary sorting criteria. In Python, expand the `ascending` list. In SQL, add to the `ORDER BY` clause inside the window function.",
                "data": pd.DataFrame({
                    "user_id": [101, 101, 101, 102, 102],
                    "email": ["old@a.com", "apple@a.com", "zebra@a.com", "first@b.com", "second@b.com"],
                    "updated_at": [
                        "2023-01-01", "2023-02-15", "2023-02-15", 
                        "2023-04-20", "2023-04-20"
                    ]
                }),
                "evaluation_criteria": [
                    "Can modify existing sorting logic to accommodate multiple columns with different directional sorts (one descending by time, another descending alphabetically)",
                    "Understands tie-breaker mechanics"
                ],
                "solution_code": """\\
df["updated_at"] = pd.to_datetime(df["updated_at"])
df = df.sort_values(by=["user_id", "updated_at", "email"], ascending=[True, False, False])
result = df.drop_duplicates(subset=["user_id"], keep="first").reset_index(drop=True)
""",
                "solution_sql": """
WITH RankedUsers AS (
    SELECT 
        user_id,
        email,
        updated_at,
        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY updated_at DESC, email DESC) as rn
    FROM user_records
)
SELECT 
    user_id,
    email,
    updated_at
FROM RankedUsers
WHERE rn = 1
ORDER BY user_id;
""",
                "expected_output": pd.DataFrame({
                    "user_id": [101, 102],
                    "email": ["zebra@a.com", "second@b.com"],
                    "updated_at": pd.to_datetime(["2023-02-15", "2023-04-20"])
                }),
                "big_o_explanation": "Time Complexity: O(N log N). Adding an extra column (`email`) to the sort conditions slightly increases overhead during the sort comparisons but the overall complexity remains asymptotically O(N log N). Space Complexity: O(N) to keep the records in memory for final evaluation. The optimization here is consolidating all determinism rules into a single pass of the sorting algorithm rather than running secondary filtering passes.",
                "follow_up_probes": [
                    "If we used `RANK()` here instead of `ROW_NUMBER()`, would the result change?",
                    "Could we use `MAX() OVER()` combined with a `CASE` statement instead of sorting?"
                ]
            }
        ]
    }
