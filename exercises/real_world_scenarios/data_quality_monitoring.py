import pandas as pd
import numpy as np

def get_exercise():
    base_data = pd.DataFrame({
        "run_id": [1, 2, 3, 4, 5, 6],
        "pipeline_name": ["orders_etl", "users_etl", "payments_etl", "orders_etl", "users_etl", "payments_etl"],
        "run_date": ["2024-03-01", "2024-03-01", "2024-03-01", "2024-03-02", "2024-03-02", "2024-03-02"],
        "rows_processed": [10000, 5000, 8000, 12000, 4800, 0],
        "null_count": [250, 50, 600, 120, 20, 0],
        "duplicate_count": [80, 10, 200, 50, 5, 0],
        "status": ["success", "success", "partial", "success", "success", "failed"],
        "duration_seconds": [120, 90, 180, 115, 85, 5]
    })

    return {
        "title": "Data Quality & Pipeline Monitoring",
        "subtitle": "Defensive Engineering, Anomaly Detection, Rolling Stats",
        "description": "A data platform team discovers that dashboards are showing incorrect numbers. Investigation reveals data quality issues in upstream pipelines: \"Can you build automated data quality checks and a pipeline monitoring summary?\" This tests defensive engineering, anomaly detection, and operational awareness — what separates mid-level from senior DEs.",
        "difficulty_level": "mid_to_senior",
        "source_inspiration": "Airbnb, Uber, Google · Interview Query, Exponent",
        "data": base_data,
        "table_name": "pipeline_runs",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "Divide `null_count` by `rows_processed` (and multiply by 100) to get `null_rate`. Do the same for `duplicate_count`. Use `round()` to clean up the output. Watch out for division-by-zero if `rows_processed` is 0.",
        "hint_sql": "Use CASE WHEN rows_processed = 0 THEN NULL ELSE ROUND(...) END to compute null_rate and duplicate_rate.",
        "solution_python": """\
import numpy as np
df["run_date"] = pd.to_datetime(df["run_date"])
safe_rows = df["rows_processed"].replace(0, np.nan)
df["null_rate"] = ((df["null_count"] / safe_rows) * 100).round(2)
df["duplicate_rate"] = ((df["duplicate_count"] / safe_rows) * 100).round(2)

result = df[["run_id", "pipeline_name", "run_date", "rows_processed", "null_count", "duplicate_count", "null_rate", "duplicate_rate"]].copy()
result = result.sort_values(["run_date", "pipeline_name"]).reset_index(drop=True)
""",
        "solution_sql": """\
SELECT
    run_id,
    pipeline_name,
    CAST(run_date AS DATE) AS run_date,
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
""",
        "deep_dive": "Data quality monitoring often involves aggregating raw logging data to derive metrics. Defensive engineering principles include explicitly handling zero division and building robust exception checks (e.g., failed statuses vs metric thresholds).",
        "big_o_explanation": "Time Complexity: O(N) for vectorized calculations in pandas / table scans in SQL. Space Complexity: O(N) for adding derived columns.",
        "mcq_questions": [
            {
                "question": "What is data lineage and why does it matter?",
                "stage_number": 1,
                "options": [
                    {"label": "A", "text": "The physical location of data on disk", "is_correct": False},
                    {"label": "B", "text": "Tracking data's origin, transformations, and downstream dependencies end-to-end", "is_correct": True},
                    {"label": "C", "text": "The order in which tables were created", "is_correct": False},
                    {"label": "D", "text": "A tool for compressing data", "is_correct": False}
                ],
                "explanation": "Data lineage maps where data comes from (sources), how it's transformed (ETL steps), and where it goes (downstream tables, dashboards). When a dashboard shows wrong numbers, lineage lets you trace backwards: \"This dashboard reads from mart_revenue, which is built by dbt_revenue_model...\" — pinpointing exactly where the bug is."
            },
            {
                "question": "What's the difference between Great Expectations, dbt tests, and custom validation scripts?",
                "stage_number": 2,
                "options": [
                    {"label": "A", "text": "They are all identical tools", "is_correct": False},
                    {"label": "B", "text": "Great Expectations is a dedicated framework; dbt tests are embedded in transformation; custom scripts are ad-hoc", "is_correct": True},
                    {"label": "C", "text": "dbt tests can only check for nulls", "is_correct": False},
                    {"label": "D", "text": "Great Expectations only works with Spark", "is_correct": False}
                ],
                "explanation": "Great Expectations: Dedicated framework with 300+ built-in expectations. dbt tests: YAML-based tests (unique, not_null, accepted_values) run as part of transformation logic. Custom scripts: Python/SQL validation in Airflow operators."
            },
            {
                "question": "What is 'data observability'?",
                "stage_number": 3,
                "options": [
                    {"label": "A", "text": "Viewing data in a dashboard", "is_correct": False},
                    {"label": "B", "text": "Monitoring freshness, volume, schema, distribution, and lineage", "is_correct": True},
                    {"label": "C", "text": "A type of database index", "is_correct": False},
                    {"label": "D", "text": "Real-time streaming of all data changes", "is_correct": False}
                ],
                "explanation": "Data observability borrows from software observability (metrics, logs, traces). Pillars include: Freshness, Volume (Stage 3 anomaly detection), Schema, Distribution, and Lineage."
            },
            {
                "question": "What is the 'circuit breaker' pattern in data pipelines?",
                "stage_number": 4,
                "options": [
                    {"label": "A", "text": "A hardware component that prevents electrical overload", "is_correct": False},
                    {"label": "B", "text": "An automatic mechanism that stops downstream processing when upstream quality drops", "is_correct": True},
                    {"label": "C", "text": "A way to split pipelines into parallel branches", "is_correct": False},
                    {"label": "D", "text": "A technique for compressing pipeline outputs", "is_correct": False}
                ],
                "explanation": "Circuit breakers halt a pipeline if assertions fail (e.g., row count > 1000), preventing bad data from propagating to dashboards. Implemented via Airflow ShortCircuitOperator or dbt standard error thresholds."
            }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Null & Duplicate Detection",
                "scenario": "The data platform team has been asked to produce a daily data quality scorecard. For each pipeline on each run date, calculate the null_rate (null_count / rows_processed) and duplicate_rate (duplicate_count / rows_processed) as percentages rounded to 2 decimal places.",
                "hint": "Divide null_count by rows_processed (and multiply by 100). Use round() or ROUND(). Watch out for division by zero.",
                "data": base_data,
                "evaluation_criteria": [
                    "Handles division by zero gracefully",
                    "Multiplies by 100 for percentages",
                    "Distinguishes count vs rate"
                ],
                "solution_code": """\
import numpy as np
df["run_date"] = pd.to_datetime(df["run_date"])
safe_rows = df["rows_processed"].replace(0, np.nan)
df["null_rate"] = ((df["null_count"] / safe_rows) * 100).round(2)
df["duplicate_rate"] = ((df["duplicate_count"] / safe_rows) * 100).round(2)

result = df[["run_id", "pipeline_name", "run_date", "rows_processed", "null_count", "duplicate_count", "null_rate", "duplicate_rate"]].copy()
result = result.sort_values(["run_date", "pipeline_name"]).reset_index(drop=True)
""",
                "solution_sql": """\
SELECT
    run_id,
    pipeline_name,
    CAST(run_date AS TIMESTAMP) AS run_date,
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
""",
                "expected_output": pd.DataFrame({
                    "run_id": [1, 3, 2, 4, 6, 5],
                    "pipeline_name": ["orders_etl", "payments_etl", "users_etl", "orders_etl", "payments_etl", "users_etl"],
                    "run_date": pd.to_datetime(["2024-03-01", "2024-03-01", "2024-03-01", "2024-03-02", "2024-03-02", "2024-03-02"]),
                    "rows_processed": [10000, 8000, 5000, 12000, 0, 4800],
                    "null_count": [250, 600, 50, 120, 0, 20],
                    "duplicate_count": [80, 200, 10, 50, 0, 5],
                    "null_rate": [2.50, 7.50, 1.00, 1.00, float('nan'), 0.42],
                    "duplicate_rate": [0.80, 2.50, 0.20, 0.42, float('nan'), 0.10]
                }),
                "big_o_explanation": "**Time:** O(N) single-pass vectorized operations\n**Space:** O(N) to hold derived rate columns",
                "follow_up_probes": [
                    "What happens in pandas if you divide by zero without replacing zeros first?",
                    "At what null_rate threshold would you stop downstream processing?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Flag Data Quality Violations",
                "scenario": "Leadership wants a simple traffic-light system. Add a quality_flag column: mark a run as 'violation' if null_rate > 5% OR duplicate_rate > 2%, and 'ok' otherwise. Runs with status = 'failed' should always be flagged as 'failed_run'.",
                "hint": "Use np.select() with conditions checked in order: status=='failed', then rate thresholds. In SQL, use multiple CASE WHEN lines.",
                "data": base_data,
                "evaluation_criteria": [
                    "Correct condition ordering (failed status has precedence)",
                    "Correctly uses OR logic for multiple thresholds",
                    "Handles default fallback logic"
                ],
                "solution_code": """\
import numpy as np
df["run_date"] = pd.to_datetime(df["run_date"])
safe_rows = df["rows_processed"].replace(0, np.nan)
df["null_rate"] = ((df["null_count"] / safe_rows) * 100).round(2)
df["duplicate_rate"] = ((df["duplicate_count"] / safe_rows) * 100).round(2)

conditions = [
    df["status"] == "failed",
    (df["null_rate"] > 5) | (df["duplicate_rate"] > 2)
]
choices = ["failed_run", "violation"]
df["quality_flag"] = np.select(conditions, choices, default="ok")

result = df[["run_id", "pipeline_name", "run_date", "null_rate", "duplicate_rate", "status", "quality_flag"]].copy()
result = result.sort_values(["run_date", "pipeline_name"]).reset_index(drop=True)
""",
                "solution_sql": """\
WITH Rates AS (
    SELECT
        run_id,
        pipeline_name,
        CAST(run_date AS TIMESTAMP) AS run_date,
        status,
        CASE WHEN rows_processed = 0 THEN NULL
             ELSE ROUND(null_count * 100.0 / rows_processed, 2) END AS null_rate,
        CASE WHEN rows_processed = 0 THEN NULL
             ELSE ROUND(duplicate_count * 100.0 / rows_processed, 2) END AS duplicate_rate
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
        WHEN status = 'failed' THEN 'failed_run'
        WHEN null_rate > 5 OR duplicate_rate > 2 THEN 'violation'
        ELSE 'ok'
    END AS quality_flag
FROM Rates
ORDER BY run_date, pipeline_name;
""",
                "expected_output": pd.DataFrame({
                    "run_id": [1, 3, 2, 4, 6, 5],
                    "pipeline_name": ["orders_etl", "payments_etl", "users_etl", "orders_etl", "payments_etl", "users_etl"],
                    "run_date": pd.to_datetime(["2024-03-01", "2024-03-01", "2024-03-01", "2024-03-02", "2024-03-02", "2024-03-02"]),
                    "null_rate": [2.50, 7.50, 1.00, 1.00, float('nan'), 0.42],
                    "duplicate_rate": [0.80, 2.50, 0.20, 0.42, float('nan'), 0.10],
                    "status": ["success", "partial", "success", "success", "failed", "success"],
                    "quality_flag": ["ok", "violation", "ok", "ok", "failed_run", "ok"]
                }),
                "big_o_explanation": "**Time:** O(N) vectorized conditions via np.select()\n**Space:** O(N) for column persistence",
                "follow_up_probes": [
                    "Why does the order of conditions matter?",
                    "How would you integrate this logic to page an on-call engineer?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Anomaly Detection (Z-Score)",
                "scenario": "Catch sudden pipeline volume spikes: compute a 7-day rolling mean and std_dev of rows_processed for 'orders_etl', and flag runs where the Z-score is > 2 standard deviations away.",
                "hint": "Use df.rolling(window=7, min_periods=3). In SQL, use AVG() OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW).",
                "data": pd.DataFrame({
                    "run_id": [1, 2, 3, 4, 5, 6, 7, 8],
                    "pipeline_name": ["orders_etl"] * 8,
                    "run_date": ["2024-03-01", "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-08"],
                    "rows_processed": [11000, 10800, 11200, 10900, 11100, 11050, 950, 11200],
                    "null_count": [100, 90, 110, 95, 105, 98, 800, 102],
                    "duplicate_count": [50, 45, 55, 48, 52, 50, 400, 51],
                    "status": ["success", "success", "success", "success", "success", "success", "partial", "success"],
                    "duration_seconds": [120, 118, 122, 119, 121, 120, 300, 121]
                }),
                "evaluation_criteria": [
                    "Proper window definition (7 days prior + current limit, min periods 3)",
                    "Correct formulation of Z-Score formula",
                    "Absolute value threshold check |Z| > 2"
                ],
                "solution_code": """\
orders = df[df["pipeline_name"] == "orders_etl"].copy()
orders["run_date"] = pd.to_datetime(orders["run_date"])
orders = orders.sort_values("run_date").reset_index(drop=True)

orders["rolling_mean"] = orders["rows_processed"].rolling(window=7, min_periods=3).mean().round(2)
orders["rolling_std"] = orders["rows_processed"].rolling(window=7, min_periods=3).std().round(2)

orders["z_score"] = ((orders["rows_processed"] - orders["rolling_mean"]) / orders["rolling_std"]).round(3)

orders["is_anomaly"] = orders["z_score"].abs() > 2

# Fill nan with False so tests can match it clearly, but actually pandas does False for nan > 2, lets fill is_anomaly
orders["is_anomaly"] = orders["is_anomaly"].fillna(False)

result = orders[["run_id", "pipeline_name", "run_date", "rows_processed",
                  "rolling_mean", "rolling_std", "z_score", "is_anomaly"]].copy()
result = result.reset_index(drop=True)
""",
                "solution_sql": """\
WITH RollingStats AS (
    SELECT
        run_id,
        pipeline_name,
        CAST(run_date AS TIMESTAMP) AS run_date,
        rows_processed,
        AVG(rows_processed) OVER (
            PARTITION BY pipeline_name
            ORDER BY run_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS raw_rolling_mean,
        STDDEV_SAMP(rows_processed) OVER (
            PARTITION BY pipeline_name
            ORDER BY run_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS raw_rolling_std,
        COUNT(rows_processed) OVER (
            PARTITION BY pipeline_name
            ORDER BY run_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as cnt
    FROM pipeline_runs
    WHERE pipeline_name = 'orders_etl'
)
SELECT
    run_id,
    pipeline_name,
    run_date,
    rows_processed,
    CASE WHEN cnt < 3 THEN NULL ELSE ROUND(raw_rolling_mean, 2) END AS rolling_mean,
    CASE WHEN cnt < 3 THEN NULL ELSE ROUND(raw_rolling_std, 2) END AS rolling_std,
    CASE
        WHEN cnt < 3 OR raw_rolling_std IS NULL OR raw_rolling_std = 0 THEN NULL
        ELSE ROUND((rows_processed - raw_rolling_mean) / raw_rolling_std, 3)
    END AS z_score,
    CASE
        WHEN cnt < 3 OR raw_rolling_std IS NULL OR raw_rolling_std = 0 THEN FALSE
        WHEN ABS((rows_processed - raw_rolling_mean) / raw_rolling_std) > 2 THEN TRUE
        ELSE FALSE
    END AS is_anomaly
FROM RollingStats
ORDER BY run_date;
""",
                "expected_output": pd.DataFrame({
                    "run_id": [1, 2, 3, 4, 5, 6, 7, 8],
                    "pipeline_name": ["orders_etl"] * 8,
                    "run_date": pd.to_datetime(["2024-03-01", "2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-08"]),
                    "rows_processed": [11000, 10800, 11200, 10900, 11100, 11050, 950, 11200],
                    "rolling_mean": [float('nan'), float('nan'), 11000.00, 10975.00, 11000.00, 11008.33, 9571.43, 9600.00],
                    "rolling_std": [float('nan'), float('nan'), 200.00, 170.78, 158.11, 142.89, 3803.93, 3817.18],
                    "z_score": [float('nan'), float('nan'), 1.000, -0.439, 0.632, 0.292, -2.266, 0.419],
                    "is_anomaly": [False, False, False, False, False, False, True, False]
                }),
                "big_o_explanation": "**Time:** O(N) optimized with C-level rolling window implementation.\n**Space:** O(N) new metric fields over dataset.",
                "follow_up_probes": [
                    "Why min_periods=3?",
                    "What happens if std_dev is precisely 0?",
                    "Why use sample std deviation instead of population?"
                ]
            },
            {
                "stage_number": 4,
                "title": "SLA Monitoring Summary",
                "scenario": "Define SLA compliance as: status = 'success' AND duration_seconds < 300. Compute: weekly runs, weekly SLA-compliant runs, compliance rate, and average duration per pipeline. Label the week over week trend as 'improving', 'degrading', or 'stable'. Return only the latest week per pipeline.",
                "hint": "Assign ISO week number, aggregate by pipeline_name and week, use lag or shift for trend comparison.",
                "data": pd.DataFrame({
                    "run_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                    "pipeline_name": ["orders_etl"] * 8 + ["users_etl"] * 8,
                    "run_date": ["2024-03-04", "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-11", "2024-03-12", "2024-03-13", "2024-03-14",
                                 "2024-03-04", "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-11", "2024-03-12", "2024-03-13", "2024-03-14"],
                    "rows_processed": [11000, 10800, 11200, 10900, 11100, 11050, 11300, 11200, 5000, 4900, 4800, 5100, 5000, 5200, 4950, 5100],
                    "null_count": [100, 90, 110, 95, 105, 98, 102, 108, 50, 45, 60, 55, 48, 52, 47, 50],
                    "duplicate_count": [50, 45, 55, 48, 52, 50, 51, 53, 10, 8, 12, 11, 9, 10, 9, 10],
                    "status": ["success", "success", "success", "success", "success", "success", "success", "success",
                               "success", "success", "failed", "success", "success", "success", "success", "success"],
                    "duration_seconds": [240, 260, 280, 310, 220, 215, 218, 222, 90, 88, 400, 95, 92, 88, 91, 89]
                }),
                "evaluation_criteria": [
                    "Correctly formulates conjunction rules for SLA",
                    "Proper week extraction and grouping",
                    "Applies lookback comparison avoiding off-by-one errors"
                ],
                "solution_code": """\
df["run_date"] = pd.to_datetime(df["run_date"])

# Use dt.isocalendar().week 
df["week"] = df["run_date"].dt.isocalendar().week.astype(int)
df["sla_met"] = (df["status"] == "success") & (df["duration_seconds"] < 300)

weekly = df.groupby(["pipeline_name", "week"]).agg(
    total_runs=("run_id", "count"),
    sla_runs=("sla_met", "sum"),
    avg_duration=("duration_seconds", "mean")
).reset_index()
weekly["compliance_rate"] = (weekly["sla_runs"] / weekly["total_runs"] * 100).round(1)

weekly = weekly.sort_values(["pipeline_name", "week"])
weekly["prev_compliance"] = weekly.groupby("pipeline_name")["compliance_rate"].shift(1)

def get_trend(r):
    if pd.isna(r["prev_compliance"]):
        return "stable"
    if r["compliance_rate"] > r["prev_compliance"]:
        return "improving"
    elif r["compliance_rate"] < r["prev_compliance"]:
        return "degrading"
    return "stable"

weekly["trend"] = weekly.apply(get_trend, axis=1)

# latest week summary
result = weekly.sort_values("week").groupby("pipeline_name").tail(1).reset_index(drop=True)
result["avg_duration"] = result["avg_duration"].round(1)
result = result[["pipeline_name", "total_runs", "sla_runs", "compliance_rate", "avg_duration", "trend"]].copy()
result = result.sort_values("pipeline_name").reset_index(drop=True)
""",
                "solution_sql": """\
WITH WeeklyStats AS (
    SELECT
        pipeline_name,
        -- DuckDB supports DATE_TRUNC with 'week' or YEARWEEK/STRFTIME, handle compatible cast
        CAST(DATE_TRUNC('week', CAST(run_date AS DATE)) AS DATE) AS week_start,
        COUNT(*) AS total_runs,
        SUM(CASE WHEN status = 'success' AND duration_seconds < 300 THEN 1 ELSE 0 END) AS sla_runs,
        ROUND(AVG(duration_seconds), 1) AS avg_duration,
        ROUND(
            SUM(CASE WHEN status = 'success' AND duration_seconds < 300 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1
        ) AS compliance_rate
    FROM pipeline_runs
    GROUP BY pipeline_name, DATE_TRUNC('week', CAST(run_date AS DATE))
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
            WHEN prev_compliance IS NULL THEN 'stable'
            WHEN compliance_rate > prev_compliance THEN 'improving'
            WHEN compliance_rate < prev_compliance THEN 'degrading'
            ELSE 'stable'
        END AS trend,
        ROW_NUMBER() OVER (PARTITION BY pipeline_name ORDER BY week_start DESC) AS rn
    FROM WithTrend
)
SELECT pipeline_name, total_runs, sla_runs, compliance_rate, avg_duration, CAST(trend AS VARCHAR) AS trend
FROM Ranked
WHERE rn = 1
ORDER BY pipeline_name;
""",
                "expected_output": pd.DataFrame({
                    "pipeline_name": ["orders_etl", "users_etl"],
                    "total_runs": [4, 4],
                    "sla_runs": [4, 4],
                    "compliance_rate": [100.0, 100.0],
                    "avg_duration": [218.8, 90.0],
                    "trend": ["improving", "improving"]
                }),
                "big_o_explanation": "**Time:** O(N log N) for grouping and lag function processing\n**Space:** O(W * P) where W is weeks and P is pipelines for summary aggregations",
                "follow_up_probes": [
                    "What happens if there are empty weeks? How do you maintain continuous SLA?",
                    "Difference between p99 latency vs average latency?"
                ]
            }
        ]
    }
