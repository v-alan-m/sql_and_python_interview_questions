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
FROM table_name
GROUP BY user_id;
""",
        "deep_dive": "Deduplication via Hash Aggregation (`GROUP BY` and `MIN`) processes in O(N) time complexity, making it highly efficient. Sorting the data and dropping duplicates takes O(N log N) time due to the sorting overhead. However, sorting is sometimes required if we need to retrieve the entire row associated with the minimum date rather than just the minimum value itself."
    }
