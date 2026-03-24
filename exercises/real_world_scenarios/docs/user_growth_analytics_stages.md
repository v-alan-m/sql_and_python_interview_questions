# Scenario 1: User Growth Analytics Dashboard

**Source Inspiration:** DataLemur (Twitter Histogram, Facebook Active Users) · Meta, Spotify, Netflix
**Level Range:** Entry → Mid
**Description:** A social media platform needs to measure user growth. The product team asks: "Can you build a data model showing how our user base has grown over time, broken down by acquisition channel?"

## Data Schema (`raw_signups`)
| Column | Type | Description |
|--------|------|-------------|
| user_id | int | Unique user identifier |
| signup_date | str (date) | Date user signed up |
| channel | str | Acquisition channel: "organic", "paid_ads", "referral", "social_media" |
| country | str | User's country |

---
## Stages

### Stage 1: Daily Signup Counts
**Level:** Entry
**Key Concepts:** `GROUP BY`, `COUNT()`
**Scenario:** To begin modeling our user growth, we first need to know how many new users are joining each day. Calculate the total number of signups per day from the `raw_signups` data.
**Coding Task:** Count new signups per day from raw data.

**Python Solution:**
```python
df["signup_date"] = pd.to_datetime(df["signup_date"])
df = df.groupby("signup_date", as_index=False)["user_id"].count()
df = df.rename(columns={"user_id": "daily_signups"})
df = df.sort_values("signup_date").reset_index(drop=True)
result = df
```

**SQL Solution:**
```sql
SELECT 
    signup_date, 
    COUNT(user_id) AS daily_signups
FROM raw_signups
GROUP BY signup_date
ORDER BY signup_date ASC;
```

**Expected Output Data Shape:** `signup_date`, `daily_signups`

---
### Stage 2: Cumulative User Growth
**Level:** Entry
**Key Concepts:** `cumsum()`, `SUM() OVER()` window
**Scenario:** Now that we have daily signup counts, we need to show the total size of our user base over time. Calculate the cumulative running total of users day by day.
**Coding Task:** Add running total of users over time.

**Python Solution:**
```python
df["signup_date"] = pd.to_datetime(df["signup_date"])
daily = df.groupby("signup_date", as_index=False)["user_id"].count().rename(columns={"user_id": "daily_signups"})
daily = daily.sort_values("signup_date").reset_index(drop=True)
daily["total_users"] = daily["daily_signups"].cumsum()
result = daily
```

**SQL Solution:**
```sql
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
ORDER BY signup_date ASC;
```

**Expected Output Data Shape:** `signup_date`, `daily_signups`, `total_users`

---
### Stage 3: Growth Rate Calculation
**Level:** Mid
**Key Concepts:** `.pct_change()`, `LAG()`
**Scenario:** The product team wants to know if growth is accelerating or flattening. Calculate the day-over-day growth rate percentage for our daily signups.
**Coding Task:** Calculate day-over-day growth rate %.

**Python Solution:**
```python
df["signup_date"] = pd.to_datetime(df["signup_date"])
daily = df.groupby("signup_date", as_index=False)["user_id"].count().rename(columns={"user_id": "daily_signups"})
daily = daily.sort_values("signup_date").reset_index(drop=True)
daily["growth_rate_pct"] = daily["daily_signups"].pct_change() * 100
daily["growth_rate_pct"] = daily["growth_rate_pct"].fillna(0.0).round(2)
result = daily
```

**SQL Solution:**
```sql
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
ORDER BY signup_date ASC;
```

**Expected Output Data Shape:** `signup_date`, `daily_signups`, `growth_rate_pct`

---
### Stage 4: Channel-Segmented Growth
**Level:** Mid
**Key Concepts:** `PARTITION BY`, grouped cumsum
**Scenario:** Finally, we want to see which acquisition channels are driving the most long-term growth. Calculate the cumulative running total of users, broken down by both date and channel.
**Coding Task:** Break down cumulative growth by acquisition channel.

**Python Solution:**
```python
df["signup_date"] = pd.to_datetime(df["signup_date"])
channel_daily = df.groupby(["signup_date", "channel"], as_index=False)["user_id"].count().rename(columns={"user_id": "daily_signups"})
channel_daily = channel_daily.sort_values(["channel", "signup_date"]).reset_index(drop=True)
channel_daily["channel_total_users"] = channel_daily.groupby("channel")["daily_signups"].cumsum()
result = channel_daily.sort_values(["signup_date", "channel"]).reset_index(drop=True)
```

**SQL Solution:**
```sql
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
ORDER BY signup_date ASC, channel ASC;
```

**Expected Output Data Shape:** `signup_date`, `channel`, `daily_signups`, `channel_total_users`

---
## MCQ Bank

**Q1 (Stage 1):** *"What is the difference between a fact table and a dimension table?"*
- A) Fact tables store descriptive attributes; dimension tables store measurements (Incorrect)
- B) Fact tables store quantitative measurements; dimension tables store descriptive context (Correct)
- C) Both store the same types of data but are partitioned differently (Incorrect)
- D) Dimension tables are always larger than fact tables (Incorrect)
- **Explanation:** Fact tables contain numeric, additive measures (revenue, counts, quantities) and foreign keys. Dimension tables provide the "who, what, when, where" context — e.g., `dim_user`, `dim_date`, `dim_channel`. In our scenario, `raw_signups` would feed into a `fact_daily_signups` table (measures: signup_count) joined to `dim_date` and `dim_channel` (descriptive context).

**Q2 (Stage 2):** *"In a star schema, what sits at the center?"*
- A) A dimension table (Incorrect)
- B) A staging table (Incorrect)
- C) A fact table (Correct)
- D) A bridge table (Incorrect)
- **Explanation:** A star schema has a central **fact table** surrounded by **dimension tables** connected via foreign keys. It's called "star" because the diagram resembles a star with the fact table at the center and dimensions radiating outward. Unlike a snowflake schema, dimension tables in a star schema are fully denormalized (no sub-dimensions).

**Q3 (Stage 3):** *"When would you use a snowflake schema instead of a star schema?"*
- A) When you want faster query performance (Incorrect)
- B) When dimension tables have deeply hierarchical attributes that benefit from normalisation (Correct)
- C) When you have a small dataset (Incorrect)
- D) Snowflake schemas are always preferred over star schemas (Incorrect)
- **Explanation:** Snowflake schemas normalize dimension tables into sub-tables (e.g., `dim_product` → `dim_category` → `dim_department`). This saves storage and improves data integrity for large, hierarchical dimensions, but adds JOIN complexity and slows queries. Star schemas are preferred for BI/dashboards where read speed matters most.

**Q4 (Stage 4):** *"What is the 'grain' of a fact table?"*
- A) The smallest unit of data stored in each row (Correct)
- B) The total number of rows in the table (Incorrect)
- C) The number of dimension tables it connects to (Incorrect)
- D) The compression ratio of the table (Incorrect)
- **Explanation:** Grain defines what **one row** represents. For `fact_daily_signups`, the grain is "one signup count per day per channel." Getting the grain wrong causes double-counting or missed data. Always declare the grain before designing joins — it's the first question a Kimball-methodology data warehouse architect answers.
