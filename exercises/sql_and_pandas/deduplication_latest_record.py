import pandas as pd

def get_exercise():
    return {
        "title": "Deduplication (Latest Record)",
        "description": "Given a dataset of user logins, remove duplicate entries for each user, keeping ONLY their most recent login based on the 'login_timestamp'.",
        "data": pd.DataFrame({
            "user_id": [1, 2, 1, 3, 2],
            "login_timestamp": [
                "2023-01-01 10:00:00", 
                "2023-01-01 11:30:00", 
                "2023-01-02 09:15:00", 
                "2023-01-02 14:00:00", 
                "2023-01-01 08:00:00"
            ]
        }),
        "table_name": "user_logins",
        "allowed_modes": ["Python", "SQL"],
        "hint_python": "Convert the timestamp column to datetime. Sort the DataFrame by timestamp, then use `drop_duplicates()` specifying the subset and the `keep` parameter.",
        "hint_sql": "Use the `ROW_NUMBER()` window function grouped (`PARTITION BY`) by the user ID, ordering by the timestamp in descending order.",
        "solution_python": '''\n# 1. Ensure datetime type\ndf["login_timestamp"] = pd.to_datetime(df["login_timestamp"])\n\n# 2. Sort by timestamp, then drop duplicates keeping the last one (latest)\nresult = df.sort_values("login_timestamp").drop_duplicates(subset=["user_id"], keep="last")\n''',
        "solution_sql": '''\nWITH RankedLogins AS (\n    SELECT \n        user_id, \n        login_timestamp,\n        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_timestamp DESC) as rank\n    FROM user_logins\n)\nSELECT \n    user_id, \n    login_timestamp \nFROM RankedLogins \nWHERE rank = 1;\n''',
        "deep_dive": "In Pandas, `drop_duplicates` is heavily optimized in C, making it incredibly fast: O(N log N) dominated by the initial sorting. In SQL, utilizing `ROW_NUMBER()` is a widely established pattern for handling Slowly Changing Dimensions (SCD Type 2) or isolating 'last-known-good' states. It outperforms explicit `GROUP BY MAX()` self-joins on larger datasets heavily favored in massive distributed databases like Snowflake.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Basic Timestamp Max",
                "scenario": "We just need to know the latest login time for each user. Return a dataframe containing only the user_id and their most recent login timestamp.",
                "hint": "Use a group-by operation to find the maximum timestamp for each user.",
                "data": pd.DataFrame({
                    "user_id": [1, 2, 1, 3, 2],
                    "login_timestamp": [
                        "2023-01-01 10:00:00", 
                        "2023-01-01 11:30:00", 
                        "2023-01-02 09:15:00", 
                        "2023-01-02 14:00:00", 
                        "2023-01-01 08:00:00"
                    ]
                }),
                "evaluation_criteria": [
                    "Candidate understands basic aggregation grouping by user_id.",
                    "Candidate computes the maximum login_timestamp correctly."
                ],
                "solution_code": """\\
df["login_timestamp"] = pd.to_datetime(df["login_timestamp"])
result = df.groupby("user_id", as_index=False)["login_timestamp"].max()
""",
                "solution_sql": """
SELECT 
    user_id, 
    MAX(login_timestamp) AS login_timestamp
FROM user_logins
GROUP BY user_id
ORDER BY user_id;
""",
                "expected_output": pd.DataFrame({
                    "user_id": [1, 2, 3],
                    "login_timestamp": pd.to_datetime([
                        "2023-01-02 09:15:00", 
                        "2023-01-01 11:30:00", 
                        "2023-01-02 14:00:00"
                    ])
                }),
                "follow_up_probes": [
                    "What is the time complexity of this operation in Python and SQL?",
                    "If a user logged in exactly at the same time from two different devices, what does this output?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Full Record Deduplication",
                "scenario": "Now we need the ENTIRE login record (including the device type) for the latest login. A simple GROUP BY MAX won't work anymore without joins. How can you get the full row?",
                "hint": "Sort the data by the timestamp first, then use a strategy to drop duplicate rows based on user_id while keeping the last occurrence. In SQL, use the ROW_NUMBER() window function.",
                "data": pd.DataFrame({
                    "user_id": [1, 2, 1, 3, 2],
                    "login_timestamp": [
                        "2023-01-01 10:00:00", 
                        "2023-01-01 11:30:00", 
                        "2023-01-02 09:15:00", 
                        "2023-01-02 14:00:00", 
                        "2023-01-01 08:00:00"
                    ],
                    "device_type": ["Mobile", "Tablet", "Desktop", "Desktop", "Mobile"]
                }),
                "evaluation_criteria": [
                    "Candidate recognizes that retaining other columns requires a different approach than simple aggregation.",
                    "In Python, candidate uses `sort_values` followed by `drop_duplicates(keep='last')`.",
                    "In SQL, candidate utilizes `ROW_NUMBER() OVER(PARTITION BY ... ORDER BY ... DESC)`."
                ],
                "solution_code": """\\
df["login_timestamp"] = pd.to_datetime(df["login_timestamp"])
result = df.sort_values(["user_id", "login_timestamp"]).drop_duplicates(subset=["user_id"], keep="last").reset_index(drop=True)
""",
                "solution_sql": """
WITH RankedLogins AS (
    SELECT 
        user_id, 
        login_timestamp,
        device_type,
        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_timestamp DESC) as rank
    FROM user_logins
)
SELECT 
    user_id, 
    login_timestamp,
    device_type
FROM RankedLogins 
WHERE rank = 1
ORDER BY user_id;
""",
                "expected_output": pd.DataFrame({
                    "user_id": [1, 2, 3],
                    "login_timestamp": pd.to_datetime([
                        "2023-01-02 09:15:00", 
                        "2023-01-01 11:30:00", 
                        "2023-01-02 14:00:00"
                    ]),
                    "device_type": ["Desktop", "Tablet", "Desktop"]
                }),
                "follow_up_probes": [
                    "Why is `ROW_NUMBER()` preferred over a self-join with a subquery of max timestamps in modern data warehouses?",
                    "How does the performance of sorting compare to a hash-based group by?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Handling Ties",
                "scenario": "What if a user's device sends two login events at the EXACT same second? We want the deduplication to be deterministic. If timestamps are tied, prioritize the login based on 'device_type' alphabetically descending (e.g., 'Mobile' beats 'Desktop').",
                "hint": "You need to add a secondary sorting key to your existing logic.",
                "data": pd.DataFrame({
                    "user_id": [1, 1, 2, 3],
                    "login_timestamp": [
                        "2023-01-02 09:15:00", 
                        "2023-01-02 09:15:00", 
                        "2023-01-01 11:30:00", 
                        "2023-01-02 14:00:00"
                    ],
                    "device_type": ["Desktop", "Mobile", "Tablet", "Desktop"]
                }),
                "evaluation_criteria": [
                    "Candidate successfully implements multiple sorting conditions.",
                    "Candidate correctly considers the sort order required to make 'Mobile' (M) rank higher than 'Desktop' (D) when kept last or ranked number one."
                ],
                "solution_code": """\\
df["login_timestamp"] = pd.to_datetime(df["login_timestamp"])
result = df.sort_values(["user_id", "login_timestamp", "device_type"]).drop_duplicates(subset=["user_id"], keep="last").reset_index(drop=True)
""",
                "solution_sql": """
WITH RankedLogins AS (
    SELECT 
        user_id, 
        login_timestamp,
        device_type,
        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_timestamp DESC, device_type DESC) as rank
    FROM user_logins
)
SELECT 
    user_id, 
    login_timestamp,
    device_type
FROM RankedLogins 
WHERE rank = 1
ORDER BY user_id;
""",
                "expected_output": pd.DataFrame({
                    "user_id": [1, 2, 3],
                    "login_timestamp": pd.to_datetime([
                        "2023-01-02 09:15:00", 
                        "2023-01-01 11:30:00", 
                        "2023-01-02 14:00:00"
                    ]),
                    "device_type": ["Mobile", "Tablet", "Desktop"]
                }),
                "follow_up_probes": [
                    "Are sorting operations stable in Pandas / SQL by default?",
                    "What if there are 3 fully identical rows with the exact same timestamp and device_type, does your solution still work perfectly?"
                ]
            }
        ]
    }
