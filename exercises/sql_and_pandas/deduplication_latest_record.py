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
        "allowed_modes": ["Python", "SQL"],
        "hint_python": "Convert the timestamp column to datetime. Sort the DataFrame by timestamp, then use `drop_duplicates()` specifying the subset and the `keep` parameter.",
        "hint_sql": "Use the `ROW_NUMBER()` window function grouped (`PARTITION BY`) by the user ID, ordering by the timestamp in descending order.",
        "solution_python": '''\n# 1. Ensure datetime type\ndf["login_timestamp"] = pd.to_datetime(df["login_timestamp"])\n\n# 2. Sort by timestamp, then drop duplicates keeping the last one (latest)\nresult_df = df.sort_values("login_timestamp").drop_duplicates(subset=["user_id"], keep="last")\n''',
        "solution_sql": '''\nWITH RankedLogins AS (\n    SELECT \n        user_id, \n        login_timestamp,\n        ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_timestamp DESC) as rank\n    FROM df\n)\nSELECT \n    user_id, \n    login_timestamp \nFROM RankedLogins \nWHERE rank = 1;\n''',
        "deep_dive": "In Pandas, `drop_duplicates` is heavily optimized in C, making it incredibly fast: O(N log N) dominated by the initial sorting. In SQL, utilizing `ROW_NUMBER()` is a widely established pattern for handling Slowly Changing Dimensions (SCD Type 2) or isolating 'last-known-good' states. It outperforms explicit `GROUP BY MAX()` self-joins on larger datasets heavily favored in massive distributed databases like Snowflake."
    }
