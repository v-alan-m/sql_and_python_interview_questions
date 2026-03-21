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
        "deep_dive": "The Python `drop_duplicates` backed by sorting is highly readable. The sort dictates the O(N log N) performance hit. In SQL, the `ROW_NUMBER()` function allows us to maintain the entire row's context (like the email) while aggregating based on another column (`updated_at`). Using a simple `GROUP BY` and `MAX(updated_at)` makes it hard to fetch the correct corresponding email if multiple emails exist per user, which is why window functions are superior for contextual deduplication."
    }
