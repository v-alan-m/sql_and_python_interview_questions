import pandas as pd

def get_exercise():
    base_data = pd.DataFrame({
        "user_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "signup_date": ["2023-01-01", "2023-01-01", "2023-01-02", "2023-01-02", "2023-01-02", "2023-01-03", "2023-01-03", "2023-01-03", "2023-01-03", "2023-01-03"],
        "channel": ["organic", "organic", "paid_ads", "paid_ads", "referral", "social_media", "social_media", "organic", "referral", "paid_ads"],
        "country": ["US", "US", "US", "US", "US", "US", "US", "US", "US", "US"]
    })

    return {
        "title": "User Growth Analytics Dashboard",
        "subtitle": "Cumulative Aggregation, Window Functions, Dimensional Modeling",
        "description": "A social media platform needs to measure user growth. The product team asks: \"Can you build a data model showing how our user base has grown over time, broken down by acquisition channel?\"",
        "difficulty_level": "entry_to_mid",
        "source_inspiration": "DataLemur (Twitter Histogram, Facebook Active Users) · Meta, Spotify, Netflix",
        "data": base_data,
        "table_name": "raw_signups",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "First use pd.to_datetime on signup_date, then group by the date and count.",
        "hint_sql": "Use the COUNT() window function and GROUP BY signup_date.",
        "solution_python": """\
df["signup_date"] = pd.to_datetime(df["signup_date"])
df = df.groupby("signup_date", as_index=False)["user_id"].count()
df = df.rename(columns={"user_id": "daily_signups"})
df = df.sort_values("signup_date").reset_index(drop=True)
result = df""",
        "solution_sql": """\
SELECT 
    signup_date, 
    COUNT(user_id) AS daily_signups
FROM raw_signups
GROUP BY signup_date
ORDER BY signup_date ASC;""",
        "deep_dive": "Calculations of daily signups involve simple group by aggregations. The cumsum starts building upon this by iterating through the grouped values.",
        "big_o_explanation": "Grouping takes **O(N)** time. Sorting takes **O(K log K)** time where K is the number of unique days.",
        "mcq_questions": [
            {
                "question": "What is the difference between a fact table and a dimension table?",
                "stage_number": 1,
                "options": [
                    {"label": "A", "text": "Fact tables store descriptive attributes; dimension tables store measurements", "is_correct": False},
                    {"label": "B", "text": "Fact tables store quantitative measurements; dimension tables store descriptive context", "is_correct": True},
                    {"label": "C", "text": "Both store the same types of data but are partitioned differently", "is_correct": False},
                    {"label": "D", "text": "Dimension tables are always larger than fact tables", "is_correct": False}
                ],
                "explanation": "Fact tables contain numeric, additive measures (revenue, counts, quantities) and foreign keys. Dimension tables provide the \"who, what, when, where\" context \u2014 e.g., dim_user, dim_date, dim_channel. In our scenario, raw_signups would feed into a fact_daily_signups table (measures: signup_count) joined to dim_date and dim_channel (descriptive context)."
            },
            {
                "question": "In a star schema, what sits at the center?",
                "stage_number": 2,
                "options": [
                    {"label": "A", "text": "A dimension table", "is_correct": False},
                    {"label": "B", "text": "A staging table", "is_correct": False},
                    {"label": "C", "text": "A fact table", "is_correct": True},
                    {"label": "D", "text": "A bridge table", "is_correct": False}
                ],
                "explanation": "A star schema has a central fact table surrounded by dimension tables connected via foreign keys. It's called \"star\" because the diagram resembles a star with the fact table at the center and dimensions radiating outward. Unlike a snowflake schema, dimension tables in a star schema are fully denormalized (no sub-dimensions)."
            },
            {
                "question": "When would you use a snowflake schema instead of a star schema?",
                "stage_number": 3,
                "options": [
                    {"label": "A", "text": "When you want faster query performance", "is_correct": False},
                    {"label": "B", "text": "When dimension tables have deeply hierarchical attributes that benefit from normalisation", "is_correct": True},
                    {"label": "C", "text": "When you have a small dataset", "is_correct": False},
                    {"label": "D", "text": "Snowflake schemas are always preferred over star schemas", "is_correct": False}
                ],
                "explanation": "Snowflake schemas normalize dimension tables into sub-tables (e.g., dim_product -> dim_category -> dim_department). This saves storage and improves data integrity for large, hierarchical dimensions, but adds JOIN complexity and slows queries. Star schemas are preferred for BI/dashboards where read speed matters most."
            },
            {
                "question": "What is the 'grain' of a fact table?",
                "stage_number": 4,
                "options": [
                    {"label": "A", "text": "The smallest unit of data stored in each row", "is_correct": True},
                    {"label": "B", "text": "The total number of rows in the table", "is_correct": False},
                    {"label": "C", "text": "The number of dimension tables it connects to", "is_correct": False},
                    {"label": "D", "text": "The compression ratio of the table", "is_correct": False}
                ],
                "explanation": "Grain defines what one row represents. For fact_daily_signups, the grain is \"one signup count per day per channel.\" Getting the grain wrong causes double-counting or missed data. Always declare the grain before designing joins \u2014 it's the first question a Kimball-methodology data warehouse architect answers."
            }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Daily Signup Counts",
                "scenario": "To begin modeling our user growth, we first need to know how many new users are joining each day. Calculate the total number of signups per day from the raw_signups data.",
                "hint": "Use GROUP BY signup_date and counting user_id.",
                "data": base_data,
                "evaluation_criteria": [
                    "Ability to use COUNT or size aggregations properly.",
                    "Correct date conversion mapping natively."
                ],
                "solution_code": """\
df["signup_date"] = pd.to_datetime(df["signup_date"])
df = df.groupby("signup_date", as_index=False)["user_id"].count()
df = df.rename(columns={"user_id": "daily_signups"})
df = df.sort_values("signup_date").reset_index(drop=True)
result = df""",
                "solution_sql": """\
SELECT 
    signup_date, 
    COUNT(user_id) AS daily_signups
FROM raw_signups
GROUP BY signup_date
ORDER BY signup_date ASC;""",
                "expected_output": pd.DataFrame({
                    "signup_date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
                    "daily_signups": [2, 3, 5]
                }),
                "big_o_explanation": "**Time Complexity:** **O(N)** for processing group iterations per unique row representation.\n**Space Complexity:** **O(K)** for the daily aggregation grouping.",
                "follow_up_probes": [
                    "How might the grain apply if timezone issues are present?",
                    "What happens to days without signups?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Cumulative User Growth",
                "scenario": "Now that we have daily signup counts, we need to show the total size of our user base over time. Calculate the cumulative running total of users day by day.",
                "hint": "Apply cumsum() on the daily signups.",
                "data": base_data,
                "evaluation_criteria": [
                    "Knowledge of cumulative distribution formulas.",
                    "Ability to aggregate properly and sort data to align cumulative calculations incrementally."
                ],
                "solution_code": """\
df["signup_date"] = pd.to_datetime(df["signup_date"])
daily = df.groupby("signup_date", as_index=False)["user_id"].count().rename(columns={"user_id": "daily_signups"})
daily = daily.sort_values("signup_date").reset_index(drop=True)
daily["total_users"] = daily["daily_signups"].cumsum()
result = daily""",
                "solution_sql": """\
WITH DailyCounts AS (
    SELECT 
        signup_date, 
        COUNT(user_id) AS daily_signups
    FROM raw_signups
    GROUP BY signup_date
)
SELECT 
    signup_date, 
    daily_signups,
    SUM(daily_signups) OVER (ORDER BY signup_date ASC) AS total_users
FROM DailyCounts
ORDER BY signup_date ASC;""",
                "expected_output": pd.DataFrame({
                    "signup_date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
                    "daily_signups": [2, 3, 5],
                    "total_users": [2, 5, 10]
                }),
                "big_o_explanation": "**Time Complexity:** **O(N + K log K)**. Evaluating cumulative sums runs linearly O(K) where the aggregation takes O(N) over raw data length.\n**Space Complexity:** **O(K)** to retain the new resulting dataframe grouping.",
                "follow_up_probes": [
                    "How could this window aggregate behave if there is missing daily data?",
                    "Under the hood, what is the impact of O(K log K) when adding more years of data?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Growth Rate Calculation",
                "scenario": "The product team wants to know if growth is accelerating or flattening. Calculate the day-over-day growth rate percentage for our daily signups.",
                "hint": "Use pct_change() along with filling missing initial zero items handling.",
                "data": base_data,
                "evaluation_criteria": [
                    "Capability of calculating row to row variation logic.",
                    "Using window frames efficiently to check rate changes."
                ],
                "solution_code": """\
df["signup_date"] = pd.to_datetime(df["signup_date"])
daily = df.groupby("signup_date", as_index=False)["user_id"].count().rename(columns={"user_id": "daily_signups"})
daily = daily.sort_values("signup_date").reset_index(drop=True)
daily["growth_rate_pct"] = daily["daily_signups"].pct_change() * 100
daily["growth_rate_pct"] = daily["growth_rate_pct"].fillna(0.0).round(2)
result = daily""",
                "solution_sql": """\
WITH DailyCounts AS (
    SELECT 
        signup_date, 
        COUNT(user_id) AS daily_signups
    FROM raw_signups
    GROUP BY signup_date
)
SELECT 
    signup_date, 
    daily_signups,
    COALESCE(
        ROUND(
            (daily_signups - LAG(daily_signups) OVER (ORDER BY signup_date ASC)) 
            * 100.0 / LAG(daily_signups) OVER (ORDER BY signup_date ASC), 
            2
        ), 
        0.0
    ) AS growth_rate_pct
FROM DailyCounts
ORDER BY signup_date ASC;""",
                "expected_output": pd.DataFrame({
                    "signup_date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
                    "daily_signups": [2, 3, 5],
                    "growth_rate_pct": [0.0, 50.0, 66.67]
                }),
                "big_o_explanation": "**Time Complexity:** **O(N + K log K)** because grouping sorting is taking O(K log K).\n**Space Complexity:** **O(K)** storing one grouped object.",
                "follow_up_probes": [
                    "How would a rolling average instead help smoothing variance compared to day over day?"
                ]
            },
            {
                "stage_number": 4,
                "title": "Channel-Segmented Growth",
                "scenario": "Finally, we want to see which acquisition channels are driving the most long-term growth. Calculate the cumulative running total of users, broken down by both date and channel.",
                "hint": "Group by multiple columns, calculate running sum with cumulative distributions grouping per individual sub group partition.",
                "data": base_data,
                "evaluation_criteria": [
                    "Grouping aggregations among partitioned frames separately.",
                    "Correct matching dimensional hierarchies avoiding global cumsums."
                ],
                "solution_code": """\
df["signup_date"] = pd.to_datetime(df["signup_date"])
channel_daily = df.groupby(["signup_date", "channel"], as_index=False)["user_id"].count().rename(columns={"user_id": "daily_signups"})
channel_daily = channel_daily.sort_values(["channel", "signup_date"]).reset_index(drop=True)
channel_daily["channel_total_users"] = channel_daily.groupby("channel")["daily_signups"].cumsum()
result = channel_daily.sort_values(["signup_date", "channel"]).reset_index(drop=True)""",
                "solution_sql": """\
WITH DailyChannelCounts AS (
    SELECT 
        signup_date,
        channel,
        COUNT(user_id) AS daily_signups
    FROM raw_signups
    GROUP BY signup_date, channel
)
SELECT 
    signup_date,
    channel,
    daily_signups,
    SUM(daily_signups) OVER (PARTITION BY channel ORDER BY signup_date ASC) AS channel_total_users
FROM DailyChannelCounts
ORDER BY signup_date ASC, channel ASC;""",
                "expected_output": pd.DataFrame({
                    "signup_date": pd.to_datetime([
                        "2023-01-01", "2023-01-02", "2023-01-02", 
                        "2023-01-03", "2023-01-03", "2023-01-03", "2023-01-03"
                    ]),
                    "channel": [
                        "organic", "paid_ads", "referral", 
                        "organic", "paid_ads", "referral", "social_media"
                    ],
                    "daily_signups": [2, 2, 1, 1, 1, 1, 2],
                    "channel_total_users": [2, 2, 1, 3, 3, 2, 2]
                }),
                "big_o_explanation": "**Time Complexity:** **O(N + C log C)** where C relates closely representing combinatorial daily and segment records per dimensions.\n**Space Complexity:** **O(C)** creating individual segmentations dimensions values.",
                "follow_up_probes": [
                    "How are partitioning and indexing affecting query processing when data scales into millions of combinations?",
                    "If dimensional arrays explode in scale, how could memory bounds exceed expectations compared to grouped sums?"
                ]
            }
        ]
    }
