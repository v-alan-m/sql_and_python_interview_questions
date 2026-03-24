# Scenario 4: Data Quality & Pipeline Monitoring

**Source Inspiration:** Airbnb, Uber, Google · Interview Query, Exponent
**Level Range:** Mid → Senior
**Description:** A data platform team discovers that dashboards are showing incorrect numbers. Investigation reveals data quality issues in upstream pipelines: "Can you build automated data quality checks and a pipeline monitoring summary?" This tests defensive engineering, anomaly detection, and operational awareness — what separates mid-level from senior DEs.

## Data Schema (`pipeline_runs`)
| Column | Type | Description |
|--------|------|-------------|
| run_id | int | Unique pipeline run identifier |
| pipeline_name | str | Name: "orders_etl", "users_etl", "payments_etl" |
| run_date | str (date) | Date of the run |
| rows_processed | int | Number of rows processed |
| null_count | int | Number of null values detected |
| duplicate_count | int | Number of duplicate rows found |
| status | str | "success", "failed", "partial" |
| duration_seconds | int | How long the run took |

---
## Stages

### Stage 1: Null & Duplicate Detection
**Level:** Mid
**Key Concepts:** Ratio calculations, `groupby`, derived metric columns
**Scenario:** The data platform team has been asked to produce a daily data quality scorecard. For each pipeline on each run date, calculate the `null_rate` (null_count / rows_processed) and `duplicate_rate` (duplicate_count / rows_processed) as percentages rounded to 2 decimal places. This scorecard will be the foundation for all downstream quality checks.
**Coding Task:** Calculate null_rate and duplicate_rate per pipeline per day.

**Hint:** Divide `null_count` by `rows_processed` (and multiply by 100) to get `null_rate`. Do the same for `duplicate_count`. Use `round()` to clean up the output. Watch out for division-by-zero if `rows_processed` is 0.

**Sample Data:**
```
run_id | pipeline_name  | run_date   | rows_processed | null_count | duplicate_count | status  | duration_seconds
1      | orders_etl     | 2024-03-01 | 10000          | 250        | 80              | success | 120
2      | users_etl      | 2024-03-01 | 5000           | 50         | 10              | success | 90
3      | payments_etl   | 2024-03-01 | 8000           | 600        | 200             | partial | 180
4      | orders_etl     | 2024-03-02 | 12000          | 120        | 50              | success | 115
5      | users_etl      | 2024-03-02 | 4800           | 20         | 5               | success | 85
6      | payments_etl   | 2024-03-02 | 0              | 0          | 0               | failed  | 5
```

**Python Solution:**
```python
df["run_date"] = pd.to_datetime(df["run_date"])

# Avoid division by zero
safe_rows = df["rows_processed"].replace(0, pd.NA)

df["null_rate"] = ((df["null_count"] / safe_rows) * 100).round(2)
df["duplicate_rate"] = ((df["duplicate_count"] / safe_rows) * 100).round(2)

result = df[["run_id", "pipeline_name", "run_date", "rows_processed",
             "null_count", "duplicate_count", "null_rate", "duplicate_rate"]].copy()
result = result.sort_values(["run_date", "pipeline_name"]).reset_index(drop=True)
```

**SQL Solution:**
```sql
SELECT
    run_id,
    pipeline_name,
    run_date,
    rows_processed,
    null_count,
    duplicate_count,
    CASE
        WHEN rows_processed = 0 THEN NULL
        ELSE ROUND(null_count * 100.0 / rows_processed, 2)
    END AS null_rate,
    CASE
        WHEN rows_processed = 0 THEN NULL
        ELSE ROUND(duplicate_count * 100.0 / rows_processed, 2)
    END AS duplicate_rate
FROM pipeline_runs
ORDER BY run_date, pipeline_name;
```

**Expected Output Data Shape:** `run_id`, `pipeline_name`, `run_date`, `rows_processed`, `null_count`, `duplicate_count`, `null_rate`, `duplicate_rate`
- run_id 1 (orders_etl, Mar 1): null_rate = 2.50%, duplicate_rate = 0.80%
- run_id 3 (payments_etl, Mar 1): null_rate = 7.50%, duplicate_rate = 2.50%
- run_id 6 (payments_etl, Mar 2): rows_processed = 0 → null_rate = NULL, duplicate_rate = NULL

**Big-O Analysis:**
- **Time:** O(N) — single-pass vectorized division across all rows
- **Space:** O(N) for the two new derived columns added to the DataFrame

**Evaluation Criteria:**
- Handles division-by-zero gracefully (failed runs with 0 rows_processed)
- Multiplies by 100 to express as a percentage (not a decimal fraction)
- Does not confuse `null_count` (a raw count) with `null_rate` (a ratio)

**Follow-Up Probes:**
- "What happens in pandas if you divide by zero without replacing zeros first? How does `pd.NA` differ from `np.nan` here?"
- "At what null_rate threshold would you stop downstream processing? How would you implement that as an Airflow sensor?"
- "How would you store this scorecard in a data warehouse to track trends over time?"

---
### Stage 2: Flag Data Quality Violations
**Level:** Mid
**Key Concepts:** Conditional column creation, `np.select()`, `CASE WHEN`, multi-condition thresholds
**Scenario:** Leadership wants a simple traffic-light system. Using the rates computed in Stage 1, add a `quality_flag` column: mark a run as **"violation"** if `null_rate > 5%` OR `duplicate_rate > 2%`, and **"ok"** otherwise. Runs with `status = "failed"` should always be flagged as **"failed_run"** regardless of rates.
**Coding Task:** Mark rows where null_rate > 5% or duplicate_rate > 2% as "violation"; handle failed runs separately.

**Hint:** Use `np.select()` with an ordered list of conditions — check `status == "failed"` first, then check rate thresholds, then default to "ok". Order matters because `np.select()` evaluates conditions top-to-bottom and stops at the first match.

**Sample Data:**
```
run_id | pipeline_name  | run_date   | rows_processed | null_count | duplicate_count | status  | duration_seconds
1      | orders_etl     | 2024-03-01 | 10000          | 250        | 80              | success | 120
2      | users_etl      | 2024-03-01 | 5000           | 50         | 10              | success | 90
3      | payments_etl   | 2024-03-01 | 8000           | 600        | 200             | partial | 180
4      | orders_etl     | 2024-03-02 | 12000          | 120        | 50              | success | 115
5      | users_etl      | 2024-03-02 | 4800           | 20         | 5               | success | 85
6      | payments_etl   | 2024-03-02 | 0              | 0          | 0               | failed  | 5
```

**Python Solution:**
```python
import numpy as np

df["run_date"] = pd.to_datetime(df["run_date"])
safe_rows = df["rows_processed"].replace(0, pd.NA)
df["null_rate"] = ((df["null_count"] / safe_rows) * 100).round(2)
df["duplicate_rate"] = ((df["duplicate_count"] / safe_rows) * 100).round(2)

conditions = [
    df["status"] == "failed",
    (df["null_rate"] > 5) | (df["duplicate_rate"] > 2),
]
choices = ["failed_run", "violation"]
df["quality_flag"] = np.select(conditions, choices, default="ok")

result = df[["run_id", "pipeline_name", "run_date", "null_rate",
             "duplicate_rate", "status", "quality_flag"]].copy()
result = result.sort_values(["run_date", "pipeline_name"]).reset_index(drop=True)
```

**SQL Solution:**
```sql
WITH Rates AS (
    SELECT
        run_id,
        pipeline_name,
        run_date,
        status,
        CASE WHEN rows_processed = 0 THEN NULL
             ELSE ROUND(null_count * 100.0 / rows_processed, 2)
        END AS null_rate,
        CASE WHEN rows_processed = 0 THEN NULL
             ELSE ROUND(duplicate_count * 100.0 / rows_processed, 2)
        END AS duplicate_rate
    FROM pipeline_runs
)
SELECT
    run_id,
    pipeline_name,
    run_date,
    null_rate,
    duplicate_rate,
    status,
    CASE
        WHEN status = 'failed'                         THEN 'failed_run'
        WHEN null_rate > 5 OR duplicate_rate > 2       THEN 'violation'
        ELSE 'ok'
    END AS quality_flag
FROM Rates
ORDER BY run_date, pipeline_name;
```

**Expected Output Data Shape:** `run_id`, `pipeline_name`, `run_date`, `null_rate`, `duplicate_rate`, `status`, `quality_flag`
- run_id 1 (orders_etl): null_rate 2.50%, dup_rate 0.80% → "ok"
- run_id 3 (payments_etl, partial): null_rate 7.50% > 5% → "violation"
- run_id 4 (orders_etl, Mar 2): dup_rate 0.42% → "ok"
- run_id 5 (users_etl, Mar 2): dup_rate 0.10% → "ok"
- run_id 6 (payments_etl): status = "failed" → "failed_run"

**Big-O Analysis:**
- **Time:** O(N) — vectorized condition evaluation via `np.select()` over all rows
- **Space:** O(N) for the `quality_flag` series added to the DataFrame

**Evaluation Criteria:**
- Prioritizes the `status == "failed"` check before rate checks (correct ordering of conditions)
- Uses `OR` logic correctly — a single violation on either metric is sufficient to flag
- Does not flag `failed_run` rows as "violation" (even though their rates may be NULL/misleading)

**Follow-Up Probes:**
- "Why does the order of conditions in `np.select()` matter? What would happen if you checked the rate violation before the failed_run condition?"
- "How would you alert the on-call engineer when a 'violation' flag is generated? What tools would you use?"
- "Should a 'partial' status run always be flagged as a violation? What additional business rules might apply?"

---
### Stage 3: Anomaly Detection (Z-Score)
**Level:** Senior
**Key Concepts:** Rolling statistics, `rolling()`, Z-score calculation, window functions
**Scenario:** The team wants to catch sudden drops or spikes in pipeline volume that simple threshold rules miss. For the `orders_etl` pipeline, compute a **7-day rolling mean and standard deviation** of `rows_processed`, then calculate a **Z-score** for each run. Flag runs where the Z-score is outside ±2 standard deviations as `is_anomaly = True`. Z-score = (rows_processed − rolling_mean) / rolling_std.
**Coding Task:** Detect anomalous row counts using Z-score (> 2 std devs from rolling mean).

**Hint:** Use `df.rolling(window=7, min_periods=3)` to avoid NaN-heavy early rows. After computing the Z-score, flag with `abs(z_score) > 2`. In SQL, use `AVG() OVER` and `STDDEV_SAMP() OVER` with a `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` frame.

**Sample Data:**
```
run_id | pipeline_name | run_date   | rows_processed | null_count | duplicate_count | status  | duration_seconds
1      | orders_etl    | 2024-03-01 | 11000          | 100        | 50              | success | 120
2      | orders_etl    | 2024-03-02 | 10800          | 90         | 45              | success | 118
3      | orders_etl    | 2024-03-03 | 11200          | 110        | 55              | success | 122
4      | orders_etl    | 2024-03-04 | 10900          | 95         | 48              | success | 119
5      | orders_etl    | 2024-03-05 | 11100          | 105        | 52              | success | 121
6      | orders_etl    | 2024-03-06 | 11050          | 98         | 50              | success | 120
7      | orders_etl    | 2024-03-07 | 950            | 800        | 400             | partial | 300
8      | orders_etl    | 2024-03-08 | 11200          | 102        | 51              | success | 121
```

**Python Solution:**
```python
orders = df[df["pipeline_name"] == "orders_etl"].copy()
orders["run_date"] = pd.to_datetime(orders["run_date"])
orders = orders.sort_values("run_date").reset_index(drop=True)

# 7-day rolling stats (min 3 periods to avoid too many NaNs early on)
orders["rolling_mean"] = orders["rows_processed"].rolling(window=7, min_periods=3).mean().round(2)
orders["rolling_std"] = orders["rows_processed"].rolling(window=7, min_periods=3).std().round(2)

# Z-score: (value - mean) / std
orders["z_score"] = ((orders["rows_processed"] - orders["rolling_mean"]) / orders["rolling_std"]).round(3)

# Flag anomalies where |z_score| > 2
orders["is_anomaly"] = orders["z_score"].abs() > 2

result = orders[["run_id", "pipeline_name", "run_date", "rows_processed",
                  "rolling_mean", "rolling_std", "z_score", "is_anomaly"]].copy()
result = result.reset_index(drop=True)
```

**SQL Solution:**
```sql
WITH RollingStats AS (
    SELECT
        run_id,
        pipeline_name,
        run_date,
        rows_processed,
        AVG(rows_processed) OVER (
            PARTITION BY pipeline_name
            ORDER BY run_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_mean,
        STDDEV_SAMP(rows_processed) OVER (
            PARTITION BY pipeline_name
            ORDER BY run_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_std
    FROM pipeline_runs
    WHERE pipeline_name = 'orders_etl'
)
SELECT
    run_id,
    pipeline_name,
    run_date,
    rows_processed,
    ROUND(rolling_mean, 2) AS rolling_mean,
    ROUND(rolling_std, 2) AS rolling_std,
    CASE
        WHEN rolling_std IS NULL OR rolling_std = 0 THEN NULL
        ELSE ROUND((rows_processed - rolling_mean) / rolling_std, 3)
    END AS z_score,
    CASE
        WHEN rolling_std IS NULL OR rolling_std = 0 THEN FALSE
        WHEN ABS((rows_processed - rolling_mean) / rolling_std) > 2 THEN TRUE
        ELSE FALSE
    END AS is_anomaly
FROM RollingStats
ORDER BY run_date;
```

**Expected Output Data Shape:** `run_id`, `pipeline_name`, `run_date`, `rows_processed`, `rolling_mean`, `rolling_std`, `z_score`, `is_anomaly`
- run_id 1–6: rows_processed ~11,000; rolling stats stabilize; z_scores near 0 → `is_anomaly = False`
- run_id 7 (Mar 7): rows_processed = 950 vs rolling mean ~11,008; z_score ≈ -3.6 → `is_anomaly = True`
- run_id 8 (Mar 8): normal volume returns; z_score near 0 → `is_anomaly = False`

**Big-O Analysis:**
- **Time:** O(N × W) naively; O(N) with incremental rolling window implementation (pandas uses C-level sliding window)
- **Space:** O(N) for the rolling mean, std, and z_score columns; O(W) for the in-memory window state

**Evaluation Criteria:**
- Uses `rolling(min_periods=3)` or similar to avoid NaN blow-up on the first few rows
- Guards against division by zero when `rolling_std = 0` (e.g., all values identical in the window)
- Correctly interprets the Z-score threshold: flag both high spikes AND low drops (`abs(z) > 2`)
- Partitions by `pipeline_name` in SQL so each pipeline's rolling window is independent

**Follow-Up Probes:**
- "Why use `STDDEV_SAMP` rather than `STDDEV_POP` in the SQL window function?"
- "What are the limitations of Z-score-based anomaly detection? When would you use a more advanced model like Isolation Forest?"
- "How would you set up an Airflow alert to trigger a PagerDuty notification when `is_anomaly = True`?"
- "How does the choice of `min_periods` affect the trade-off between early detection and false positives?"

---
### Stage 4: SLA Monitoring Summary
**Level:** Senior
**Key Concepts:** Multi-metric aggregation, conditional aggregation, `FILTER`, SLA definition and trend reporting
**Scenario:** The engineering manager needs a weekly SLA report per pipeline. Define **SLA compliance** as: `status = "success"` AND `duration_seconds < 300`. For each `pipeline_name`, compute: total runs, SLA-compliant runs, SLA compliance rate (%), average duration, and a `trend` label — **"improving"** if compliance rate increased vs the prior week, **"degrading"** if it decreased, or **"stable"** if unchanged. Use the data below (two weeks: 2024-03-01 to 2024-03-14).
**Coding Task:** Build a per-pipeline SLA summary with trend comparison between two calendar weeks.

**Hint:** Add a `week` column using `dt.isocalendar().week` or `DATE_TRUNC('week', run_date)`. Group by `pipeline_name` + `week` to get weekly compliance rates. Then use `shift()` or `LAG()` to compare week-over-week. Finally, aggregate to a pipeline-level summary with the trend label.

**Sample Data:**
```
run_id | pipeline_name  | run_date   | rows_processed | null_count | duplicate_count | status  | duration_seconds
1      | orders_etl     | 2024-03-04 | 11000          | 100        | 50              | success | 240
2      | orders_etl     | 2024-03-05 | 10800          | 90         | 45              | success | 260
3      | orders_etl     | 2024-03-06 | 11200          | 110        | 55              | success | 280
4      | orders_etl     | 2024-03-07 | 10900          | 95         | 48              | success | 310
5      | orders_etl     | 2024-03-11 | 11100          | 105        | 52              | success | 220
6      | orders_etl     | 2024-03-12 | 11050          | 98         | 50              | success | 215
7      | orders_etl     | 2024-03-13 | 11300          | 102        | 51              | success | 218
8      | orders_etl     | 2024-03-14 | 11200          | 108        | 53              | success | 222
9      | users_etl      | 2024-03-04 | 5000           | 50         | 10              | success | 90
10     | users_etl      | 2024-03-05 | 4900           | 45         | 8               | success | 88
11     | users_etl      | 2024-03-06 | 4800           | 60         | 12              | failed  | 400
12     | users_etl      | 2024-03-07 | 5100           | 55         | 11              | success | 95
13     | users_etl      | 2024-03-11 | 5000           | 48         | 9               | success | 92
14     | users_etl      | 2024-03-12 | 5200           | 52         | 10              | success | 88
15     | users_etl      | 2024-03-13 | 4950           | 47         | 9               | success | 91
16     | users_etl      | 2024-03-14 | 5100           | 50         | 10              | success | 89
```

**Python Solution:**
```python
df["run_date"] = pd.to_datetime(df["run_date"])

# 1. Define SLA compliance per row
df["sla_met"] = (df["status"] == "success") & (df["duration_seconds"] < 300)

# 2. Assign ISO week number
df["week"] = df["run_date"].dt.isocalendar().week.astype(int)

# 3. Weekly compliance rate per pipeline
weekly = df.groupby(["pipeline_name", "week"]).agg(
    total_runs=("run_id", "count"),
    sla_runs=("sla_met", "sum"),
    avg_duration=("duration_seconds", "mean")
).reset_index()
weekly["compliance_rate"] = (weekly["sla_runs"] / weekly["total_runs"] * 100).round(1)

# 4. Compute week-over-week trend per pipeline
weekly = weekly.sort_values(["pipeline_name", "week"])
weekly["prev_compliance"] = weekly.groupby("pipeline_name")["compliance_rate"].shift(1)
weekly["trend"] = weekly.apply(
    lambda r: "improving" if pd.notna(r["prev_compliance"]) and r["compliance_rate"] > r["prev_compliance"]
              else ("degrading" if pd.notna(r["prev_compliance"]) and r["compliance_rate"] < r["prev_compliance"]
              else "stable"),
    axis=1
)

# 5. Final summary: take latest week's trend + overall stats
result = weekly.groupby("pipeline_name").apply(
    lambda g: g.sort_values("week").iloc[-1]
).reset_index(drop=True)[["pipeline_name", "total_runs", "sla_runs",
                           "compliance_rate", "avg_duration", "trend"]]
result["avg_duration"] = result["avg_duration"].round(1)
result = result.sort_values("pipeline_name").reset_index(drop=True)
```

**SQL Solution:**
```sql
WITH WeeklyStats AS (
    SELECT
        pipeline_name,
        DATE_TRUNC('week', run_date) AS week_start,
        COUNT(*) AS total_runs,
        SUM(CASE WHEN status = 'success' AND duration_seconds < 300 THEN 1 ELSE 0 END) AS sla_runs,
        ROUND(AVG(duration_seconds), 1) AS avg_duration,
        ROUND(
            SUM(CASE WHEN status = 'success' AND duration_seconds < 300 THEN 1 ELSE 0 END)
            * 100.0 / COUNT(*), 1
        ) AS compliance_rate
    FROM pipeline_runs
    GROUP BY pipeline_name, DATE_TRUNC('week', run_date)
),
WithTrend AS (
    SELECT
        pipeline_name,
        week_start,
        total_runs,
        sla_runs,
        avg_duration,
        compliance_rate,
        LAG(compliance_rate) OVER (PARTITION BY pipeline_name ORDER BY week_start) AS prev_compliance
    FROM WeeklyStats
),
Ranked AS (
    SELECT
        pipeline_name,
        week_start,
        total_runs,
        sla_runs,
        compliance_rate,
        avg_duration,
        CASE
            WHEN prev_compliance IS NULL                THEN 'stable'
            WHEN compliance_rate > prev_compliance      THEN 'improving'
            WHEN compliance_rate < prev_compliance      THEN 'degrading'
            ELSE 'stable'
        END AS trend,
        ROW_NUMBER() OVER (PARTITION BY pipeline_name ORDER BY week_start DESC) AS rn
    FROM WithTrend
)
SELECT pipeline_name, total_runs, sla_runs, compliance_rate, avg_duration, trend
FROM Ranked
WHERE rn = 1
ORDER BY pipeline_name;
```

**Expected Output Data Shape:** `pipeline_name`, `total_runs`, `sla_runs`, `compliance_rate`, `avg_duration`, `trend`
- **orders_etl:**
  - Week 10 (Mar 4–7): 4 runs, 3 sla_met (run_id 4 failed SLA with 310s), compliance_rate = 75.0%
  - Week 11 (Mar 11–14): 4 runs, 4 sla_met, compliance_rate = 100.0%
  - Final summary: trend = "improving", compliance_rate = 100.0%
- **users_etl:**
  - Week 10 (Mar 4–7): 4 runs, 3 sla_met (run_id 11 failed + > 300s), compliance_rate = 75.0%
  - Week 11 (Mar 11–14): 4 runs, 4 sla_met, compliance_rate = 100.0%
  - Final summary: trend = "improving", compliance_rate = 100.0%

**Big-O Analysis:**
- **Time:** O(N log N) — sorting by pipeline + week; aggregation and shift are O(N); overall dominated by sort
- **Space:** O(P × W) where P = distinct pipelines and W = distinct weeks; typically much smaller than N

**Evaluation Criteria:**
- Correctly defines SLA as a conjunction: `status = "success"` AND `duration_seconds < 300` (not just one condition)
- Uses `shift(1)` / `LAG()` correctly partitioned by `pipeline_name` (not across all pipelines)
- Takes the **latest week** for the trend label (not averages it across all weeks)
- Handles the first week having no previous week (→ "stable" or NULL, not an error)

**Follow-Up Probes:**
- "How would you store this SLA report in a data warehouse — as a snapshot table or a slowly changing dimension?"
- "What's the difference between p50, p95, and p99 latency, and why would you track those instead of average duration?"
- "How would you build an Airflow SLA miss callback to trigger automated alerts on SLA breaches?"
- "If a pipeline runs on weekdays only, would ISO week calculation still make sense? What alternative would you use?"

---
## MCQ Bank

**Q1 (Stage 1):** *"What is data lineage and why does it matter?"*
- A) The physical location of data on disk (Incorrect)
- B) Tracking data's origin, transformations, and downstream dependencies end-to-end (Correct)
- C) The order in which tables were created (Incorrect)
- D) A tool for compressing data (Incorrect)
- **Explanation:** Data lineage maps where data comes from (sources), how it's transformed (ETL steps), and where it goes (downstream tables, dashboards). When a dashboard shows wrong numbers, lineage lets you trace backwards: "This dashboard reads from `mart_revenue`, which is built by `dbt_revenue_model`, which reads from `stg_orders`..." — pinpointing exactly where the bug is. Tools: OpenLineage, DataHub, Atlan, dbt's built-in lineage graph. Without lineage, debugging data issues is like debugging code without a stack trace.

**Q2 (Stage 2):** *"What's the difference between Great Expectations, dbt tests, and custom validation scripts?"*
- A) They are all identical tools (Incorrect)
- B) Great Expectations is a dedicated data quality framework; dbt tests are embedded in the transformation layer; custom scripts are ad-hoc Python/SQL checks (Correct)
- C) dbt tests can only check for nulls (Incorrect)
- D) Great Expectations only works with Spark (Incorrect)
- **Explanation:** **Great Expectations (GX):** Dedicated framework with 300+ built-in expectations (`not_null`, `unique`, `between`, `regex_match`). Generates documentation and data quality reports, and can halt pipelines via checkpoint actions. **dbt tests:** YAML-based tests (`unique`, `not_null`, `accepted_values`, `relationships`) that run as part of `dbt test` — tightly coupled with transformation logic and very low overhead to add. **Custom scripts:** Python/SQL validation run in Airflow/Prefect tasks — maximum flexibility but more maintenance overhead. Production teams typically combine all three layers for defense in depth.

**Q3 (Stage 3):** *"What is 'data observability'?"*
- A) Viewing data in a dashboard (Incorrect)
- B) The ability to understand the health of data in your system by monitoring freshness, volume, schema, distribution, and lineage (Correct)
- C) A type of database index (Incorrect)
- D) Real-time streaming of all data changes (Incorrect)
- **Explanation:** Data observability borrows from software observability (metrics, logs, traces) and applies it to data pipelines. The 5 pillars are: **Freshness** (is data arriving on time?), **Volume** (are row counts normal?), **Schema** (did columns change?), **Distribution** (are values within expected ranges?), and **Lineage** (where did data come from?). Tools include Monte Carlo, Bigeye, Soda, and Elementary (open-source dbt-native). Anomaly detection (Stage 3's Z-score pattern) is the "Volume" pillar implemented from scratch.

**Q4 (Stage 4):** *"What is the 'circuit breaker' pattern in data pipelines?"*
- A) A hardware component that prevents electrical overload (Incorrect)
- B) An automatic mechanism that stops downstream processing when upstream data quality drops below a threshold (Correct)
- C) A way to split pipelines into parallel branches (Incorrect)
- D) A technique for compressing pipeline outputs (Incorrect)
- **Explanation:** If your orders pipeline produces 0 rows (normally 100K), should the downstream revenue dashboard update? No — it would wipe all revenue data. A circuit breaker checks assertions (row count > 1000, null_rate < 5%) and **halts** the pipeline if they fail, preventing bad data from propagating to dashboards and reports. Implement via Airflow's `ShortCircuitOperator`, dbt `warn`/`error` severity levels, or Great Expectations checkpoint actions. The SLA monitoring in Stage 4 feeds the same alerting pattern.
