import pandas as pd

def get_exercise():
    return {
        "title": "Deduplication",
        "description": "You are given a table of user logins containing 'user_id' and 'login_time'. Extract the earliest login time for each user, effectively deduplicating the table to show just the first login per user.",
        "data": pd.DataFrame({
            "user_id": [1, 2, 1, 3, 2, 1],
            "login_time": [
                "2023-01-01 10:00:00", 
                "2023-01-01 11:30:00", 
                "2023-01-02 09:00:00", 
                "2023-01-02 14:00:00", 
                "2023-01-03 08:00:00",
                "2022-12-31 23:59:59"
            ]
        }),
        "table_name": "user_logins",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "You can use `groupby()` on the user identifier combined with an aggregation like `min()`. Alternatively, you can sort the DataFrame by date and use `drop_duplicates()`.",
        "hint_sql": "Use the `MIN()` aggregate function combined with a `GROUP BY` clause on the user identifier, or use the `ROW_NUMBER()` window function partitioned by the user identifier.",
        "solution_python": """
# Ensure datetime type for accurate sorting/min extraction
df["login_time"] = pd.to_datetime(df["login_time"])

# Method 1: Using GroupBy aggregation
result = df.groupby("user_id", as_index=False)["login_time"].min()

# Method 2: Using Sort and Drop Duplicates
# result = df.sort_values("login_time").drop_duplicates(subset=["user_id"], keep="first")
""",
        "solution_sql": """
SELECT 
    user_id, 
    MIN(login_time) AS first_login
FROM user_logins
GROUP BY user_id;
""",
        "deep_dive": "Deduplication via Hash Aggregation (`GROUP BY` and `MIN`) processes in O(N) time complexity, making it highly efficient. Sorting the data and dropping duplicates takes O(N log N) time due to the sorting overhead. However, sorting is sometimes required if we need to retrieve the entire row associated with the minimum date rather than just the minimum value itself.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Deduplication (Aggregation)",
                "scenario": "You have a table of user logins with 'user_id' and 'login_time'. We only want to know the absolute earliest login time for each user. You don't need any other columns.",
                "hint": "Since we only need the user and the time, a simple GROUP BY and MIN() aggregation will work perfectly. In Pandas, use `groupby()` and `agg()`.",
                "data": pd.DataFrame({
                    "user_id": [1, 1, 2, 2, 3],
                    "login_time": [
                        "2023-01-02 10:00:00",
                        "2023-01-01 10:00:00",
                        "2023-01-03 10:00:00",
                        "2023-01-04 10:00:00",
                        "2023-01-01 10:00:00"
                    ]
                }),
                "evaluation_criteria": [
                    "Ability to apply basic grouping and aggregation.",
                    "Selecting the correct aggregation function (min).",
                    "Renaming aggregated columns appropriately."
                ],
                "solution_code": """\
df["login_time"] = pd.to_datetime(df["login_time"])
result = df.groupby("user_id", as_index=False).agg(first_login=("login_time", "min"))
result = result.sort_values("user_id").reset_index(drop=True)
""",
                "solution_sql": """\
SELECT 
    user_id, 
    MIN(login_time) AS first_login
FROM user_logins
GROUP BY user_id
ORDER BY user_id;
""",
                "expected_output": pd.DataFrame({
                    "user_id": [1, 2, 3],
                    "first_login": pd.to_datetime([
                        "2023-01-01 10:00:00",
                        "2023-01-03 10:00:00",
                        "2023-01-01 10:00:00"
                    ])
                }),
                "follow_up_probes": [
                    "What is the time complexity of this approach? (Expect O(N) since hashes are used for grouping).",
                    "What if the table was already sorted by user_id and login_time?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Whole Row Retrieval (Sort & Deduplicate)",
                "scenario": "Now we've added a 'device_id' column to the dataset. The analytics team wants the *entire row* associated with that first login, so we know which device they used.",
                "hint": "A simple GROUP BY won't work anymore without complicating the query. In Python, try sorting the data and dropping duplicates based on `user_id`. In SQL, use the `ROW_NUMBER()` window function.",
                "data": pd.DataFrame({
                    "user_id": [1, 1, 2, 2, 3],
                    "login_time": [
                        "2023-01-02 10:00:00",
                        "2023-01-01 10:00:00",
                        "2023-01-03 10:00:00",
                        "2023-01-04 10:00:00",
                        "2023-01-01 10:00:00"
                    ],
                    "device_id": ["mob_1", "web_1", "mob_2", "web_2", "web_3"]
                }),
                "evaluation_criteria": [
                    "Understanding the limitation of GROUP BY when needing full row context.",
                    "Using `sort_values` and `drop_duplicates(keep='first')` in Python.",
                    "Using `ROW_NUMBER()` or `RANK()` appropriately in SQL."
                ],
                "solution_code": """\
df["login_time"] = pd.to_datetime(df["login_time"])
result = df.sort_values("login_time").drop_duplicates(subset=["user_id"], keep="first")
result = result.sort_values("user_id").reset_index(drop=True)
""",
                "solution_sql": """\
WITH RankedLogins AS (
    SELECT 
        user_id, 
        login_time, 
        device_id,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_time ASC) as rn
    FROM user_logins
)
SELECT user_id, login_time, device_id
FROM RankedLogins
WHERE rn = 1
ORDER BY user_id;
""",
                "expected_output": pd.DataFrame({
                    "user_id": [1, 2, 3],
                    "login_time": pd.to_datetime([
                        "2023-01-01 10:00:00",
                        "2023-01-03 10:00:00",
                        "2023-01-01 10:00:00"
                    ]),
                    "device_id": ["web_1", "mob_2", "web_3"]
                }),
                "follow_up_probes": [
                    "Why is ROW_NUMBER() often preferred over joining back to the original table with the MIN date?",
                    "What is the new time and space complexity in Pandas due to sorting? (O(N log N))."
                ]
            },
            {
                "stage_number": 3,
                "title": "Deterministic Tie-Breaking",
                "scenario": "Sometimes a user logs in from two devices at the exact same millisecond. If we just sort by `login_time`, the `drop_duplicates` tie-breaker might be arbitrary. Force a deterministic tie-breaker by preferring the `device_id` alphabetically first.",
                "hint": "Expand your sorting criteria to include multiple columns. Both Pandas `sort_values()` and SQL `ORDER BY` in window functions can take multiple columns.",
                "data": pd.DataFrame({
                    "user_id": [1, 1, 2, 2, 2, 3, 3],
                    "login_time": [
                        "2023-01-02 10:00:00", 
                        "2023-01-01 10:00:00", 
                        "2023-01-03 10:00:00", 
                        "2023-01-03 10:00:00", 
                        "2023-01-04 10:00:00", 
                        "2023-01-01 10:00:00", 
                        "2023-01-02 10:00:00"
                    ],
                    "device_id": ["mob_1", "web_1", "web_2", "mob_2", "web_2b", "web_3", "mob_3"]
                }),
                "evaluation_criteria": [
                    "Applying multi-column sorting to handle edge case ties.",
                    "Ensuring deterministic output order."
                ],
                "solution_code": """\
df["login_time"] = pd.to_datetime(df["login_time"])
result = df.sort_values(["login_time", "device_id"]).drop_duplicates(subset=["user_id"], keep="first")
result = result.sort_values("user_id").reset_index(drop=True)
""",
                "solution_sql": """\
WITH RankedLogins AS (
    SELECT 
        user_id, 
        login_time, 
        device_id,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_time ASC, device_id ASC) as rn
    FROM user_logins
)
SELECT user_id, login_time, device_id
FROM RankedLogins
WHERE rn = 1
ORDER BY user_id;
""",
                "expected_output": pd.DataFrame({
                    "user_id": [1, 2, 3],
                    "login_time": pd.to_datetime([
                        "2023-01-01 10:00:00",
                        "2023-01-03 10:00:00",
                        "2023-01-01 10:00:00"
                    ]),
                    "device_id": ["web_1", "mob_2", "web_3"]
                }),
                "follow_up_probes": [
                    "What would happen if we used `RANK()` instead of `ROW_NUMBER()` and there was a complete duplicate row?",
                    "Can you think of any scenarios where an alphabetical tie-breaker wouldn't be appropriate?"
                ]
            },
            {
                "stage_number": 4,
                "title": "Filtering with Multiple Constraints",
                "scenario": "We've added a 'status' column ('success', 'failed'). We only want the first *successful* login. However, we still need to fetch the entire row to retrieve `device_id` and handle potential time ties via alphabetical `device_id`.",
                "hint": "You need to filter out failed logins before you prioritize and deduplicate. Where is the most efficient place to perform this filter?",
                "data": pd.DataFrame({
                    "user_id": [1, 1, 2, 2, 2, 3, 3],
                    "login_time": [
                        "2023-01-01 09:00:00", 
                        "2023-01-01 10:00:00", 
                        "2023-01-03 10:00:00", 
                        "2023-01-03 10:00:00", 
                        "2023-01-04 10:00:00", 
                        "2023-01-01 10:00:00", 
                        "2023-01-02 10:00:00"
                    ],
                    "device_id": ["mob_1", "web_1", "web_2", "mob_2", "web_2b", "web_3", "mob_3"],
                    "status": ["failed", "success", "success", "success", "success", "success", "success"]
                }),
                "evaluation_criteria": [
                    "Applying pre-filtering appropriately before window functions/sorting.",
                    "Selecting only the desired subset of data."
                ],
                "solution_code": """\
df["login_time"] = pd.to_datetime(df["login_time"])
success_df = df[df["status"] == "success"]
result = success_df.sort_values(["login_time", "device_id"]).drop_duplicates(subset=["user_id"], keep="first")
result = result.sort_values("user_id").reset_index(drop=True)
""",
                "solution_sql": """\
WITH RankedLogins AS (
    SELECT 
        user_id, 
        login_time, 
        device_id,
        status,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_time ASC, device_id ASC) as rn
    FROM user_logins
    WHERE status = 'success'
)
SELECT user_id, login_time, device_id, status
FROM RankedLogins
WHERE rn = 1
ORDER BY user_id;
""",
                "expected_output": pd.DataFrame({
                    "user_id": [1, 2, 3],
                    "login_time": pd.to_datetime([
                        "2023-01-01 10:00:00",
                        "2023-01-03 10:00:00",
                        "2023-01-01 10:00:00"
                    ]),
                    "device_id": ["web_1", "mob_2", "web_3"],
                    "status": ["success", "success", "success"]
                }),
                "follow_up_probes": [
                    "If we removed the `WHERE status = 'success'` filter but partitioned by `user_id` and `status`, how would that change the result?",
                    "Does performing the filter *before* the sort have a significant implication on performance?"
                ]
            }
        ]
    }
