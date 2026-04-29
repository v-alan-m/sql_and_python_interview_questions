# Real-World Data Engineering Scenario Designs

This document is the **blueprint/reference** for the 5 real-world DE interview scenarios. The companion system prompt (`REAL_WORLD_SCENARIOS_SYSTEM_PROMPT.md`) reads this file when generating each exercise.

---

## Research Sites for Scenario Inspiration

Use these sites to source new scenario ideas, validate difficulty levels, and attribute company origins:

| Site | URL | Extractable Fields | Best For |
|------|-----|-------------------|----------|
| **DataLemur** | [datalemur.com/questions](https://datalemur.com/questions) | Company, Title, Category, Difficulty | SQL/Python FAANG questions |
| **Interview Query** | [interviewquery.com](https://interviewquery.com) | Company, Role, Category, Difficulty | DE-specific system design + coding |
| **StrataScratch** | [stratascratch.com](https://www.stratascratch.com) | Company, Title, Difficulty, Type | Real interview Qs from 100+ companies |
| **LeetCode Database** | [leetcode.com/problemset/database](https://leetcode.com/problemset/database/) | Company, Title, Difficulty | SQL with company tags |
| **DataCamp** | [datacamp.com](https://www.datacamp.com) | Topic, Difficulty, Role Level | Conceptual + coding guides |
| **HackerRank** | [hackerrank.com/domains/sql](https://www.hackerrank.com/domains/sql) | Subdomain, Difficulty, Title | SQL challenges by subdomain |
| **Exponent** | [tryexponent.com](https://www.tryexponent.com) | Company, Category, Type | System design + DE interview |
| **Real Python** | [realpython.com](https://realpython.com) | Topic, Difficulty | Python tutorials + exercises |

---

## Scenario 1: User Growth Analytics Dashboard

**Source Inspiration:** DataLemur (Twitter Histogram, Facebook Active Users) · Meta, Spotify, Netflix
**Level Range:** Entry → Mid
**Reuses Patterns From:** `exercises/sql_and_pandas/cumulative_revenue.py`

### Business Context

A social media platform needs to measure user growth. The product team asks:
*"Can you build a data model showing how our user base has grown over time, broken down by acquisition channel?"*

This is a classic **dimensional modeling** question that tests cumulative aggregation, date handling, and fact/dimension table design.

### Data Schema

**`raw_signups` (source table)**
| Column | Type | Description |
|--------|------|-------------|
| user_id | int | Unique user identifier |
| signup_date | str (date) | Date user signed up |
| channel | str | Acquisition channel: "organic", "paid_ads", "referral", "social_media" |
| country | str | User's country |

### Stage Progression

| Stage | Level | Title | Coding Task | Key Concept |
|-------|-------|-------|-------------|-------------|
| 1 | Entry | Daily Signup Counts | Count new signups per day from raw data | `GROUP BY`, `COUNT()` |
| 2 | Entry | Cumulative User Growth | Add running total of users over time | `cumsum()`, `SUM() OVER()` window |
| 3 | Mid | Growth Rate Calculation | Calculate day-over-day growth rate % | `.pct_change()`, `LAG()` |
| 4 | Mid | Channel-Segmented Growth | Break down cumulative growth by acquisition channel | `PARTITION BY`, grouped cumsum |

### MCQ Bank

**Q1 (Stage 1):** *"What is the difference between a fact table and a dimension table?"*
- A) Fact tables store descriptive attributes; dimension tables store measurements ✗
- B) Fact tables store quantitative measurements; dimension tables store descriptive context ✓
- C) Both store the same types of data but are partitioned differently ✗
- D) Dimension tables are always larger than fact tables ✗
- **Explanation:** Fact tables contain numeric, additive measures (revenue, counts, quantities) and foreign keys. Dimension tables provide the "who, what, when, where" context — e.g., `dim_user`, `dim_date`, `dim_channel`. In our scenario, `raw_signups` would feed into a `fact_daily_signups` table (measures: signup_count) joined to `dim_date` and `dim_channel` (descriptive context).

**Q2 (Stage 2):** *"In a star schema, what sits at the center?"*
- A) A dimension table ✗
- B) A staging table ✗
- C) A fact table ✓
- D) A bridge table ✗
- **Explanation:** A star schema has a central **fact table** surrounded by **dimension tables** connected via foreign keys. It's called "star" because the diagram resembles a star with the fact table at the center and dimensions radiating outward. Unlike a snowflake schema, dimension tables in a star schema are fully denormalized (no sub-dimensions).

**Q3 (Stage 3):** *"When would you use a snowflake schema instead of a star schema?"*
- A) When you want faster query performance ✗
- B) When dimension tables have deeply hierarchical attributes that benefit from normalisation ✓
- C) When you have a small dataset ✗
- D) Snowflake schemas are always preferred over star schemas ✗
- **Explanation:** Snowflake schemas normalize dimension tables into sub-tables (e.g., `dim_product` → `dim_category` → `dim_department`). This saves storage and improves data integrity for large, hierarchical dimensions, but adds JOIN complexity and slows queries. Star schemas are preferred for BI/dashboards where read speed matters most.

**Q4 (Stage 4):** *"What is the 'grain' of a fact table?"*
- A) The smallest unit of data stored in each row ✓
- B) The total number of rows in the table ✗
- C) The number of dimension tables it connects to ✗
- D) The compression ratio of the table ✗
- **Explanation:** Grain defines what **one row** represents. For `fact_daily_signups`, the grain is "one signup count per day per channel." Getting the grain wrong causes double-counting or missed data. Always declare the grain before designing joins — it's the first question a Kimball-methodology data warehouse architect answers.

---

## Scenario 2: E-Commerce Order Pipeline — Batch vs Stream

**Source Inspiration:** Amazon, Stripe, Shopify · StrataScratch, Interview Query
**Level Range:** Entry → Mid → Senior
**Reuses Patterns From:** `exercises/sql_and_pandas/deduplication.py`, `exercises/sql_and_pandas/deduplication_latest_record.py`

### Business Context

An e-commerce company processes millions of orders daily. The data engineering team must build a pipeline that:
- Deduplicates raw order events from upstream systems
- Builds fact/dimension tables for analytics
- Handles late-arriving data and order status changes

*"Should this be a streaming pipeline or a batch pipeline? How would you handle duplicate events and late-arriving data?"*

### Data Schema

**`raw_order_events` (source table)**
| Column | Type | Description |
|--------|------|-------------|
| event_id | str | Unique event identifier |
| order_id | int | Order identifier (can repeat for status updates) |
| customer_id | int | Customer FK |
| product_id | int | Product FK |
| order_status | str | "placed", "confirmed", "shipped", "delivered", "cancelled" |
| amount | float | Order amount in USD |
| event_timestamp | str (datetime) | When the event was emitted |

### Stage Progression

| Stage | Level | Title | Coding Task | Key Concept |
|-------|-------|-------|-------------|-------------|
| 1 | Entry | Deduplicate Order Events | Remove exact-duplicate events by `event_id` | `drop_duplicates()`, `DISTINCT` |
| 2 | Mid | Latest Status Per Order | Keep only the most recent status for each order | `sort_values` + `drop_duplicates(keep='last')`, `ROW_NUMBER() OVER(PARTITION BY)` |
| 3 | Mid | Build Fact Table | Join orders with product + customer dimensions, compute total per order | Multi-table JOINs, aggregation |
| 4 | Senior | Handle Late-Arriving Data | Implement upsert/merge logic for out-of-order events | Merge logic, idempotent updates |

### MCQ Bank

**Q1 (Stage 1):** *"When should you use a streaming pipeline instead of a batch pipeline?"*
- A) Always — streaming is strictly better than batch ✗
- B) When data needs to be processed within seconds/minutes of arrival for real-time decisions ✓
- C) When you have very large historical datasets to process ✗
- D) When you want to minimise infrastructure costs ✗
- **Explanation:** Streaming pipelines (Kafka, Flink, Spark Structured Streaming) are essential when **low latency matters** — fraud detection, live dashboards, real-time recommendations. Batch pipelines (Airflow + Spark, dbt) are cheaper, simpler, and better for historical analysis, nightly ETL, and compliance reports where hours of latency are acceptable. Most production systems use a **hybrid** (Lambda/Kappa architecture).

**Q2 (Stage 2):** *"What does 'idempotency' mean in data pipelines?"*
- A) A pipeline that runs exactly once and never retries ✗
- B) A pipeline that produces the same result regardless of how many times it runs on the same input ✓
- C) A pipeline that deletes old data before writing new data ✗
- D) A pipeline that runs in parallel across multiple nodes ✗
- **Explanation:** Idempotent pipelines are **safe to retry**. If a job fails halfway and reruns, it won't create duplicates or corrupt data. Techniques include: UPSERT/MERGE instead of INSERT, writing to partitioned staging tables then atomically swapping, and using `INSERT ... ON CONFLICT DO UPDATE`. This is critical for exactly-once semantics in streaming AND batch.

**Q3 (Stage 3):** *"What is the difference between event-time and processing-time?"*
- A) Event-time is when the system processes the data; processing-time is when the event occurred ✗
- B) Event-time is when the event occurred; processing-time is when the system processes the data ✓
- C) They are the same thing in batch pipelines ✗
- D) Event-time only matters in batch systems ✗
- **Explanation:** In streaming, events can arrive **out of order** or late. A payment at 14:00:00 (event-time) might reach your pipeline at 14:05:00 (processing-time). If you window/aggregate by processing-time, results are non-deterministic. Production systems use **event-time** with **watermarks** to handle late data (e.g., "wait 5 minutes for stragglers before closing the window").

**Q4 (Stage 4):** *"What is the difference between exactly-once, at-least-once, and at-most-once delivery?"*
- A) They describe how many consumers can read a message ✗
- B) They describe delivery guarantees for how many times a message is processed ✓
- C) They describe the number of partitions in a Kafka topic ✗
- D) They only apply to batch pipelines ✗
- **Explanation:** **At-most-once:** fire and forget, may lose data. **At-least-once:** retries until acknowledged, may create duplicates (most common). **Exactly-once:** each message processed exactly once (hardest — requires idempotent consumers or transactional writes). Kafka supports exactly-once via idempotent producers + transactional consumers. Most pipelines use at-least-once + deduplication downstream.

---

## Scenario 3: Platform Engagement — Gaps & Islands

**Source Inspiration:** LinkedIn, Netflix, Spotify · DataLemur (User Streaks, Active Users)
**Level Range:** Mid → Senior
**Reuses Patterns From:** `exercises/sql_and_pandas/gaps_and_islands.py` directly

### Business Context

A streaming platform wants to understand user engagement patterns:
*"Can you identify consecutive login streaks, classify users as active/churned/re-engaged, and build a retention cohort table?"*

This tests window functions, sessionization, and advanced aggregation — core skills for any mid-to-senior DE.

### Data Schema

**`user_logins` (source table)**
| Column | Type | Description |
|--------|------|-------------|
| user_id | int | Unique user identifier |
| login_date | str (date) | Date of login activity |
| subscription_tier | str | "free", "basic", "premium" |
| signup_date | str (date) | Original signup date (for cohort analysis) |

### Stage Progression

| Stage | Level | Title | Coding Task | Key Concept |
|-------|-------|-------|-------------|-------------|
| 1 | Mid | Consecutive Login Streaks | Find start/end of each continuous login streak per user | Gaps & Islands: `diff()` + `cumsum()`, `ROW_NUMBER()` subtraction |
| 2 | Mid | User Status Classification | Label each user as "active" (logged in last 7 days), "churned" (no login 30+ days), or "at_risk" | Conditional logic on date diffs from today |
| 3 | Senior | Monthly Retention Cohort Table | Build a cohort table: for each signup month, what % of users are still active in month+1, +2, +3 | CROSS JOIN with month series, conditional aggregation |

### MCQ Bank

**Q1 (Stage 1):** *"What is a 'sessionization' problem in data engineering?"*
- A) Splitting a database into multiple sessions for performance ✗
- B) Grouping sequential user events into logical sessions based on time gaps ✓
- C) Creating user authentication sessions ✗
- D) Partitioning data by session ID ✗
- **Explanation:** Sessionization groups a stream of timestamped events into logical "sessions" — e.g., web clicks within 30 minutes of each other belong to the same session. It's a variant of the Gaps & Islands problem. In SQL, you use `LAG()` or `ROW_NUMBER()` subtraction; in Python, `diff()` + `cumsum()` with a threshold. Google Analytics, Mixpanel, and Amplitude all do this under the hood.

**Q2 (Stage 2):** *"What are DAU, WAU, and MAU and how are they typically computed?"*
- A) They are database administration metrics for query optimisation ✗
- B) Daily/Weekly/Monthly Active Users — distinct user counts within the respective time window ✓
- C) They measure data throughput in pipelines ✗
- D) They are computed using SUM() over user login counts ✗
- **Explanation:** **DAU** = distinct users active today. **WAU** = distinct users active in the last 7 days. **MAU** = distinct users active in the last 30 days. Computed via `COUNT(DISTINCT user_id) WHERE login_date BETWEEN ... AND ...`. The ratio **DAU/MAU** (called "stickiness") is a key product metric — Facebook/Meta famously targets >50%.

**Q3 (Stage 3):** *"What is a Slowly Changing Dimension (SCD) Type 2?"*
- A) A dimension that never changes ✗
- B) A dimension that overwrites old values with new values ✗
- C) A dimension that preserves history by creating a new row for each change with effective dates ✓
- D) A dimension that stores only the latest 2 versions ✗
- **Explanation:** SCD Type 2 tracks full history. When a user changes subscription from "free" to "premium", instead of overwriting, you close the old row (`effective_end = today`) and insert a new row (`effective_start = today, effective_end = NULL`). This lets you answer "What tier was user X on when they made purchase Y?" — critical for accurate historical analysis. Type 1 = overwrite (no history), Type 3 = add a "previous_value" column (limited history).

---

## Scenario 4: Data Quality & Pipeline Monitoring

**Source Inspiration:** Airbnb, Uber, Google · Interview Query, Exponent
**Level Range:** Mid → Senior
**New exercise** (builds on deduplication/validation concepts)

### Business Context

A data platform team discovers that dashboards are showing incorrect numbers. Investigation reveals data quality issues in upstream pipelines:
*"Can you build automated data quality checks and a pipeline monitoring summary?"*

This tests defensive engineering, anomaly detection, and operational awareness — what separates mid-level from senior DEs.

### Data Schema

**`pipeline_runs` (source table)**
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

### Stage Progression

| Stage | Level | Title | Coding Task | Key Concept |
|-------|-------|-------|-------------|-------------|
| 1 | Mid | Null & Duplicate Detection | Calculate null_rate and duplicate_rate per pipeline per day | Ratio calculations, `groupby` |
| 2 | Mid | Flag Data Quality Violations | Mark rows where null_rate > 5% or duplicate_rate > 2% as "violation" | Conditional column creation, `CASE WHEN` |
| 3 | Senior | Anomaly Detection (Z-Score) | Detect anomalous row counts using Z-score (> 2 std devs from rolling mean) | Rolling statistics, `rolling()`, window functions |
| 4 | Senior | SLA Monitoring Summary | Build a summary: per pipeline, days meeting SLA (< 300s), trend over time | Multi-metric aggregation, flagging |

### MCQ Bank

**Q1 (Stage 1):** *"What is data lineage and why does it matter?"*
- A) The physical location of data on disk ✗
- B) Tracking data's origin, transformations, and downstream dependencies end-to-end ✓
- C) The order in which tables were created ✗
- D) A tool for compressing data ✗
- **Explanation:** Data lineage maps where data comes from (sources), how it's transformed (ETL steps), and where it goes (downstream tables, dashboards). When a dashboard shows wrong numbers, lineage lets you trace backwards: "This dashboard reads from `mart_revenue`, which is built by `dbt_revenue_model`, which reads from `stg_orders`..." — pinpointing where the bug is. Tools: OpenLineage, DataHub, Atlan, dbt's built-in lineage graph.

**Q2 (Stage 2):** *"What's the difference between Great Expectations, dbt tests, and custom validation scripts?"*
- A) They are all identical tools ✗
- B) Great Expectations is a dedicated data quality framework; dbt tests are embedded in the transformation layer; custom scripts are ad-hoc Python/SQL checks ✓
- C) dbt tests can only check for nulls ✗
- D) Great Expectations only works with Spark ✗
- **Explanation:** **Great Expectations (GX):** Dedicated framework with 300+ built-in expectations (not_null, unique, between, regex_match). Generates documentation + data quality reports. **dbt tests:** YAML-based tests (`unique`, `not_null`, `accepted_values`, `relationships`) that run as part of `dbt test` — tightly coupled with transformation logic. **Custom scripts:** Python/SQL validation run in Airflow/Prefect tasks — maximum flexibility but more maintenance. Production teams typically combine all three.

**Q3 (Stage 3):** *"What is 'data observability'?"*
- A) Viewing data in a dashboard ✗
- B) The ability to understand the health of data in your system by monitoring freshness, volume, schema, distribution, and lineage ✓
- C) A type of database index ✗
- D) Real-time streaming of all data changes ✗
- **Explanation:** Data observability borrows from software observability (metrics, logs, traces) and applies it to data. The 5 pillars: **Freshness** (is data arriving on time?), **Volume** (are row counts normal?), **Schema** (did columns change?), **Distribution** (are values within expected ranges?), **Lineage** (where did data come from?). Tools: Monte Carlo, Bigeye, Soda, Elementary (open-source dbt-native).

**Q4 (Stage 4):** *"What is the 'circuit breaker' pattern in data pipelines?"*
- A) A hardware component that prevents electrical overload ✗
- B) An automatic mechanism that stops downstream processing when upstream data quality drops below a threshold ✓
- C) A way to split pipelines into parallel branches ✗
- D) A technique for compressing pipeline outputs ✗
- **Explanation:** If your orders pipeline produces 0 rows (normally 100K), should the downstream revenue dashboard update? No — it would wipe all revenue data. A circuit breaker checks assertions (row count > 1000, null_rate < 5%) and **halts** the pipeline if they fail, preventing bad data from propagating. Implement via Airflow `ShortCircuitOperator`, dbt `warn/error` severity, or GX checkpoint actions.

---

## Scenario 5: Revenue Data Warehouse — Star Schema Design

**Source Inspiration:** Amazon, Walmart, Instacart · DataLemur (Revenue Analysis), Interview Query
**Level Range:** Entry → Senior
**Reuses Patterns From:** `exercises/sql_and_pandas/cumulative_revenue.py`, `exercises/sql_and_pandas/daily_price_delta.py`

### Business Context

A retail company asks:
*"Design a star schema data warehouse for our sales data. Build dimension tables, a fact table, compute KPIs, and handle product price changes over time."*

This is THE classic data modeling interview question that spans entry through senior.

### Data Schema

**`raw_sales` (source table — denormalized)**
| Column | Type | Description |
|--------|------|-------------|
| transaction_id | int | Unique transaction ID |
| sale_date | str (date) | Date of sale |
| product_name | str | Product name |
| category | str | Product category |
| unit_price | float | Price per unit at time of sale |
| quantity | int | Units sold |
| customer_name | str | Customer name |
| customer_city | str | Customer's city |
| customer_tier | str | "bronze", "silver", "gold", "platinum" |

### Stage Progression

| Stage | Level | Title | Coding Task | Key Concept |
|-------|-------|-------|-------------|-------------|
| 1 | Entry | Build Dimension Tables | Extract `dim_product` and `dim_customer` from raw data with surrogate keys | Dimensional modeling basics, `factorize()` |
| 2 | Mid | Build Fact Table | Create `fact_sales` by joining dimensions, compute `total_amount` | Star schema JOINs, denormalization |
| 3 | Mid | Calculate Revenue KPIs | Compute total revenue, AOV (average order value), items per order by date | Multi-metric aggregation |
| 4 | Senior | SCD Type 2 for Price Changes | Track historical product prices with `effective_start`, `effective_end`, `is_current` | Slowly Changing Dimensions |

### MCQ Bank

**Q1 (Stage 1):** *"What are the main components of a star schema?"*
- A) One or more staging tables surrounded by raw data tables ✗
- B) A central fact table connected to multiple denormalized dimension tables via foreign keys ✓
- C) Multiple fact tables connected to each other in a chain ✗
- D) A single denormalized table containing everything ✗
- **Explanation:** A star schema's fact table sits at the center, containing measures (revenue, quantity) and foreign keys. Dimension tables radiate outward, providing context (product details, date attributes, customer info). Named "star" because the ER diagram looks like a star. It's the foundation of Kimball-methodology data warehouses and is optimized for OLAP queries with minimal JOINs.

**Q2 (Stage 2):** *"What is the difference between additive, semi-additive, and non-additive facts?"*
- A) They describe how facts can be aggregated across dimensions ✓
- B) They describe how many dimension tables connect to the fact table ✗
- C) They describe the size of the fact table ✗
- D) They are different types of primary keys ✗
- **Explanation:** **Additive facts** (revenue, quantity) can be summed across ALL dimensions (date, product, customer). **Semi-additive facts** (account balance, inventory level) can be summed across some dimensions but not time — you average or take snapshots over time instead. **Non-additive facts** (ratios, percentages, unit_price) cannot be summed meaningfully — aggregate the components, then compute the ratio.

**Q3 (Stage 3):** *"What is the difference between OLTP and OLAP?"*
- A) OLTP is for analytics; OLAP is for transactions ✗
- B) OLTP handles transactional operations (INSERT/UPDATE); OLAP handles analytical queries (aggregations, reporting) ✓
- C) They are the same thing with different names ✗
- D) OLAP systems are always slower than OLTP systems ✗
- **Explanation:** **OLTP** (Online Transaction Processing): normalized schemas (3NF), optimized for writes (INSERTs/UPDATEs), low-latency single-row operations — e.g., PostgreSQL powering a checkout page. **OLAP** (Online Analytical Processing): denormalized schemas (star/snowflake), optimized for reads (aggregations over millions of rows) — e.g., Snowflake, BigQuery, Redshift powering dashboards. Data warehouses are OLAP systems fed by OLTP sources via ETL/ELT.

**Q4 (Stage 4):** *"What is the Kimball vs Inmon methodology?"*
- A) Kimball builds top-down enterprise models; Inmon builds bottom-up dimensional marts ✗
- B) Kimball builds bottom-up dimensional data marts; Inmon builds a top-down enterprise data warehouse in 3NF first ✓
- C) They are the same methodology ✗
- D) Kimball only works with cloud data warehouses ✗
- **Explanation:** **Kimball (bottom-up):** Build star-schema data marts per business process (sales mart, inventory mart), then integrate. Faster to deliver value, business-friendly. **Inmon (top-down):** Build a single enterprise data warehouse in 3NF first, then derive data marts. More rigorous, avoids inconsistency, but slower to deliver. Most modern teams use a **hybrid**: Kimball-style star schemas built on top of a staging/raw layer (medallion architecture: bronze → silver → gold).

---

## Generating Future Scenarios

To create additional scenarios beyond these 5, follow this checklist:

### 1. Find Inspiration
Browse the research sites table above. Look for questions tagged with:
- **Companies:** FAANG, Airbnb, Uber, Stripe, Shopify, Netflix
- **Categories:** Data Modeling, ETL/ELT, Window Functions, Pipeline Design, System Design
- **Difficulty:** Medium or Hard
- **Role:** Data Engineer (not Data Analyst — focus on pipeline/modeling problems, not pure analytics)

### 2. Map to a Business Context
Every scenario should start with a **vague business question** like:
- *"Can you design a data model for X?"*
- *"How would you build a pipeline to do Y?"*
- *"We're seeing data quality issues with Z — how would you fix it?"*

### 3. Design 3–5 Progressive Stages
Follow the entry → mid → senior progression:
- **Entry stages** test: basic aggregation, filtering, GROUP BY, simple JOINs
- **Mid stages** test: window functions, CTEs, multi-table JOINs, conditional logic, deduplication
- **Senior stages** test: SCD, anomaly detection, idempotent operations, system design decisions

### 4. Create 3–4 MCQ Questions
Each MCQ should:
- Map to the conceptual knowledge behind a specific stage
- Have 4 options with exactly 1 correct answer
- Include a multi-sentence explanation covering WHY the correct answer is right and real-world context
- Reference specific tools, frameworks, or company practices where relevant

### 5. Check for Reuse
Before creating new exercise code, check existing exercises in `exercises/python/` and `exercises/sql_and_pandas/` for reusable patterns (cumulative sums, deduplication, gaps & islands, etc.).

### 6. Follow the Exercise File Convention
Use the system prompt (`REAL_WORLD_SCENARIOS_SYSTEM_PROMPT.md`) for the exact `get_exercise()` structure, including the `mcq_questions` key format.
