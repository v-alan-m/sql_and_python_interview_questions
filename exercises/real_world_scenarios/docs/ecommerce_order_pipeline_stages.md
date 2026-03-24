# Scenario 2: E-Commerce Order Pipeline — Batch vs Stream

**Source Inspiration:** Amazon, Stripe, Shopify · StrataScratch, Interview Query
**Level Range:** Entry → Mid → Senior
**Description:** An e-commerce company processes millions of orders daily. The data engineering team must build a pipeline that deduplicates raw order events, builds fact/dimension tables for analytics, and handles late-arriving data and order status changes. *"Should this be a streaming pipeline or a batch pipeline? How would you handle duplicate events and late-arriving data?"*

## Data Schema (`raw_order_events`)
| Column | Type | Description |
|--------|------|-------------|
| event_id | str | Unique event identifier |
| order_id | int | Order identifier (can repeat for status updates) |
| customer_id | int | Customer FK |
| product_id | int | Product FK |
| order_status | str | "placed", "confirmed", "shipped", "delivered", "cancelled" |
| amount | float | Order amount in USD |
| event_timestamp | str (datetime) | When the event was emitted |

---
## Stages

### Stage 1: Deduplicate Order Events
**Level:** Entry
**Key Concepts:** `drop_duplicates()`, `DISTINCT`
**Scenario:** Our upstream order service sometimes emits the same event twice due to retry logic. Before we can do any analysis, we need to remove exact-duplicate events. Deduplicate the `raw_order_events` data by `event_id`, keeping only one copy of each event.
**Coding Task:** Remove exact-duplicate events by `event_id`.

**Hint:** In Python, use `drop_duplicates()` on the `event_id` column. In SQL, use `DISTINCT` or a `GROUP BY` on `event_id` with `MIN()` on other columns.

**Sample Data:**
```
event_id | order_id | customer_id | product_id | order_status | amount | event_timestamp
E001     | 1001     | 201         | 301        | placed       | 49.99  | 2024-01-15 10:00:00
E002     | 1002     | 202         | 302        | placed       | 29.99  | 2024-01-15 10:05:00
E001     | 1001     | 201         | 301        | placed       | 49.99  | 2024-01-15 10:00:00
E003     | 1003     | 203         | 303        | placed       | 99.99  | 2024-01-15 10:10:00
E002     | 1002     | 202         | 302        | placed       | 29.99  | 2024-01-15 10:05:00
```

**Python Solution:**
```python
result = df.drop_duplicates(subset=["event_id"]).sort_values("event_id").reset_index(drop=True)
```

**SQL Solution:**
```sql
SELECT DISTINCT
    event_id,
    order_id,
    customer_id,
    product_id,
    order_status,
    amount,
    event_timestamp
FROM raw_order_events
ORDER BY event_id;
```

**Expected Output Data Shape:** `event_id`, `order_id`, `customer_id`, `product_id`, `order_status`, `amount`, `event_timestamp` — 3 rows (E001, E002, E003)

**Big-O Analysis:**
- **Time:** O(N) for hash-based deduplication in Python; O(N log N) if SQL uses sort-based DISTINCT
- **Space:** O(N) to store the hash set of seen event IDs

**Evaluation Criteria:**
- Correctly identifies `event_id` as the deduplication key
- Understands that exact duplicates share all column values
- Chooses an efficient deduplication method

**Follow-Up Probes:**
- "What if duplicates had slightly different timestamps (e.g., due to clock skew)? Would this approach still work?"
- "How would you handle deduplication at scale — millions of events per hour?"

---
### Stage 2: Latest Status Per Order
**Level:** Mid
**Key Concepts:** `sort_values` + `drop_duplicates(keep='last')`, `ROW_NUMBER() OVER(PARTITION BY)`
**Scenario:** Each order goes through multiple status transitions: placed → confirmed → shipped → delivered (or cancelled). The source table has one row per status change event. We need to find the **current** (most recent) status for each order.
**Coding Task:** Keep only the most recent status for each order based on `event_timestamp`.

**Hint:** In Python, sort by timestamp and drop duplicates on `order_id` keeping the last. In SQL, use `ROW_NUMBER()` partitioned by `order_id`, ordered by `event_timestamp DESC`.

**Sample Data:**
```
event_id | order_id | customer_id | product_id | order_status | amount | event_timestamp
E001     | 1001     | 201         | 301        | placed       | 49.99  | 2024-01-15 10:00:00
E004     | 1001     | 201         | 301        | confirmed    | 49.99  | 2024-01-15 12:00:00
E007     | 1001     | 201         | 301        | shipped      | 49.99  | 2024-01-16 09:00:00
E002     | 1002     | 202         | 302        | placed       | 29.99  | 2024-01-15 10:05:00
E005     | 1002     | 202         | 302        | confirmed    | 29.99  | 2024-01-15 14:00:00
E003     | 1003     | 203         | 303        | placed       | 99.99  | 2024-01-15 10:10:00
E006     | 1003     | 203         | 303        | cancelled    | 99.99  | 2024-01-15 16:00:00
```

**Python Solution:**
```python
df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
result = df.sort_values("event_timestamp").drop_duplicates(subset=["order_id"], keep="last")
result = result.sort_values("order_id").reset_index(drop=True)
```

**SQL Solution:**
```sql
WITH RankedEvents AS (
    SELECT
        event_id,
        order_id,
        customer_id,
        product_id,
        order_status,
        amount,
        event_timestamp,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY event_timestamp DESC) AS rn
    FROM raw_order_events
)
SELECT event_id, order_id, customer_id, product_id, order_status, amount, event_timestamp
FROM RankedEvents
WHERE rn = 1
ORDER BY order_id;
```

**Expected Output Data Shape:** `event_id`, `order_id`, `customer_id`, `product_id`, `order_status`, `amount`, `event_timestamp` — 3 rows (order 1001 → shipped, 1002 → confirmed, 1003 → cancelled)

**Big-O Analysis:**
- **Time:** O(N log N) — sorting by timestamp dominates
- **Space:** O(N) to hold the sorted intermediate result and partition state

**Evaluation Criteria:**
- Recognizes the need to sort by timestamp before deduplicating
- Correctly uses `keep='last'` (Python) or `DESC` ordering (SQL) to retain the most recent event
- Partitions correctly by `order_id`

**Follow-Up Probes:**
- "Why is `ROW_NUMBER()` preferred over `RANK()` here?"
- "What if two status events for the same order have the exact same timestamp?"
- "How does this pattern relate to Slowly Changing Dimensions (SCD Type 1)?"

---
### Stage 3: Build Fact Table
**Level:** Mid
**Key Concepts:** Multi-table JOINs, aggregation, dimensional modeling
**Scenario:** Now that we have the latest status per order, we need to join the orders with product and customer dimension tables to build a `fact_orders` table. Calculate the total revenue per customer.
**Coding Task:** Join orders with customer and product dimensions, then compute total revenue per customer.

**Hint:** In Python, use `pd.merge()` to join the tables, then `groupby()` to aggregate. In SQL, use `JOIN` and `GROUP BY`.

**Sample Data — Orders (deduplicated latest status):**
```
order_id | customer_id | product_id | order_status | amount | event_timestamp
1001     | 201         | 301        | delivered    | 49.99  | 2024-01-16 15:00:00
1002     | 202         | 302        | delivered    | 29.99  | 2024-01-17 12:00:00
1003     | 201         | 303        | delivered    | 99.99  | 2024-01-17 14:00:00
1004     | 203         | 301        | cancelled    | 49.99  | 2024-01-18 09:00:00
1005     | 202         | 304        | delivered    | 19.99  | 2024-01-18 11:00:00
```

**Sample Data — Customers (dim_customer):**
```
customer_id | customer_name | customer_city | customer_tier
201         | Alice         | New York      | gold
202         | Bob           | San Francisco | silver
203         | Charlie       | Chicago       | bronze
```

**Sample Data — Products (dim_product):**
```
product_id | product_name   | category
301        | Wireless Mouse | Electronics
302        | Python Book    | Books
303        | Standing Desk  | Furniture
304        | USB Cable      | Electronics
```

**Python Solution:**
```python
# Filter to only delivered orders
delivered = orders_df[orders_df["order_status"] == "delivered"].copy()

# Join with dimensions
fact = delivered.merge(customers_df, on="customer_id").merge(products_df, on="product_id")

# Compute total revenue per customer
result = fact.groupby(
    ["customer_id", "customer_name", "customer_city", "customer_tier"],
    as_index=False
)["amount"].sum()
result = result.rename(columns={"amount": "total_revenue"})
result = result.sort_values("customer_id").reset_index(drop=True)
```

**SQL Solution:**
```sql
SELECT
    c.customer_id,
    c.customer_name,
    c.customer_city,
    c.customer_tier,
    SUM(o.amount) AS total_revenue
FROM raw_order_events o
JOIN dim_customer c ON o.customer_id = c.customer_id
JOIN dim_product p ON o.product_id = p.product_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_id, c.customer_name, c.customer_city, c.customer_tier
ORDER BY c.customer_id;
```

**Expected Output Data Shape:** `customer_id`, `customer_name`, `customer_city`, `customer_tier`, `total_revenue` — 2 rows (Alice: 149.98, Bob: 49.98; Charlie excluded due to cancelled order)

**Big-O Analysis:**
- **Time:** O(N × M) for nested-loop JOINs, O(N + M) for hash JOINs in optimized engines, plus O(K) for aggregation (K = output groups)
- **Space:** O(N + M) for hash tables built during joins

**Evaluation Criteria:**
- Correctly filters out non-delivered orders before aggregation
- Performs JOINs on the correct foreign keys
- Aggregates revenue at the right grain (per customer)
- Understands why cancelled orders should be excluded from revenue calculations

**Follow-Up Probes:**
- "Why filter by `order_status = 'delivered'` rather than including all orders?"
- "What is the grain of this fact table?"
- "How would you handle a customer with zero delivered orders?"

---
### Stage 4: Handle Late-Arriving Data
**Level:** Senior
**Key Concepts:** Merge/upsert logic, idempotent updates, event-time ordering
**Scenario:** In production, events don't always arrive in order. A "delivered" event might arrive before the "shipped" event due to network delays. Implement an **upsert** strategy: given an existing `current_orders` snapshot and a batch of new `incoming_events`, update each order's status ONLY if the incoming event is more recent (by `event_timestamp`) than what's already stored. This ensures idempotent, out-of-order-safe updates.
**Coding Task:** Implement upsert/merge logic for out-of-order events — update only if the incoming event's timestamp is newer.

**Hint:** In Python, concatenate the existing and incoming data, then keep the row with the latest timestamp per `order_id`. In SQL, use `MERGE` or an `INSERT ... ON CONFLICT DO UPDATE` pattern with a timestamp comparison.

**Sample Data — Current Orders Snapshot:**
```
order_id | customer_id | order_status | amount | event_timestamp
1001     | 201         | confirmed    | 49.99  | 2024-01-15 12:00:00
1002     | 202         | placed       | 29.99  | 2024-01-15 10:05:00
1003     | 203         | placed       | 99.99  | 2024-01-15 10:10:00
```

**Sample Data — Incoming Events (may be out of order):**
```
order_id | customer_id | order_status | amount | event_timestamp
1001     | 201         | shipped      | 49.99  | 2024-01-16 09:00:00
1002     | 202         | confirmed    | 29.99  | 2024-01-15 14:00:00
1003     | 203         | placed       | 99.99  | 2024-01-15 08:00:00
1004     | 204         | placed       | 19.99  | 2024-01-16 10:00:00
```

**Python Solution:**
```python
current_df["event_timestamp"] = pd.to_datetime(current_df["event_timestamp"])
incoming_df["event_timestamp"] = pd.to_datetime(incoming_df["event_timestamp"])

# Concatenate current state with incoming events
combined = pd.concat([current_df, incoming_df], ignore_index=True)

# Keep the row with the latest timestamp per order (upsert logic)
combined = combined.sort_values("event_timestamp")
result = combined.drop_duplicates(subset=["order_id"], keep="last")
result = result.sort_values("order_id").reset_index(drop=True)
```

**SQL Solution:**
```sql
-- Using MERGE (upsert) pattern
MERGE INTO current_orders AS target
USING incoming_events AS source
ON target.order_id = source.order_id
WHEN MATCHED AND source.event_timestamp > target.event_timestamp THEN
    UPDATE SET
        order_status = source.order_status,
        amount = source.amount,
        event_timestamp = source.event_timestamp
WHEN NOT MATCHED THEN
    INSERT (order_id, customer_id, order_status, amount, event_timestamp)
    VALUES (source.order_id, source.customer_id, source.order_status,
            source.amount, source.event_timestamp);
```

**Expected Output Data Shape:** `order_id`, `customer_id`, `order_status`, `amount`, `event_timestamp` — 4 rows:
- 1001 → updated to "shipped" (incoming is newer)
- 1002 → updated to "confirmed" (incoming is newer)
- 1003 → stays "placed" with original timestamp (incoming is OLDER — not applied)
- 1004 → inserted as new row

**Big-O Analysis:**
- **Time:** O(N + M) for hash-based merge, O((N + M) log (N + M)) if sort-based deduplication is used
- **Space:** O(N + M) for the combined dataset

**Evaluation Criteria:**
- Implements timestamp-aware upsert — rejects stale incoming events
- Handles new orders (INSERT path) correctly
- Result is idempotent — re-running with the same incoming events produces the same output
- Understands why this matters for late-arriving/out-of-order data in production

**Follow-Up Probes:**
- "Why is the timestamp guard (`source.timestamp > target.timestamp`) critical?"
- "What would happen if you ran this merge job twice with the same incoming data?"
- "How does this relate to exactly-once vs at-least-once delivery guarantees?"
- "In a real streaming system, how would watermarks help with this problem?"

---
## MCQ Bank

**Q1 (Stage 1):** *"When should you use a streaming pipeline instead of a batch pipeline?"*
- A) Always — streaming is strictly better than batch (Incorrect)
- B) When data needs to be processed within seconds/minutes of arrival for real-time decisions (Correct)
- C) When you have very large historical datasets to process (Incorrect)
- D) When you want to minimise infrastructure costs (Incorrect)
- **Explanation:** Streaming pipelines (Kafka, Flink, Spark Structured Streaming) are essential when **low latency matters** — fraud detection, live dashboards, real-time recommendations. Batch pipelines (Airflow + Spark, dbt) are cheaper, simpler, and better for historical analysis, nightly ETL, and compliance reports where hours of latency are acceptable. Most production systems use a **hybrid** (Lambda/Kappa architecture).

**Q2 (Stage 2):** *"What does 'idempotency' mean in data pipelines?"*
- A) A pipeline that runs exactly once and never retries (Incorrect)
- B) A pipeline that produces the same result regardless of how many times it runs on the same input (Correct)
- C) A pipeline that deletes old data before writing new data (Incorrect)
- D) A pipeline that runs in parallel across multiple nodes (Incorrect)
- **Explanation:** Idempotent pipelines are **safe to retry**. If a job fails halfway and reruns, it won't create duplicates or corrupt data. Techniques include: UPSERT/MERGE instead of INSERT, writing to partitioned staging tables then atomically swapping, and using `INSERT ... ON CONFLICT DO UPDATE`. This is critical for exactly-once semantics in streaming AND batch.

**Q3 (Stage 3):** *"What is the difference between event-time and processing-time?"*
- A) Event-time is when the system processes the data; processing-time is when the event occurred (Incorrect)
- B) Event-time is when the event occurred; processing-time is when the system processes the data (Correct)
- C) They are the same thing in batch pipelines (Incorrect)
- D) Event-time only matters in batch systems (Incorrect)
- **Explanation:** In streaming, events can arrive **out of order** or late. A payment at 14:00:00 (event-time) might reach your pipeline at 14:05:00 (processing-time). If you window/aggregate by processing-time, results are non-deterministic. Production systems use **event-time** with **watermarks** to handle late data (e.g., "wait 5 minutes for stragglers before closing the window").

**Q4 (Stage 4):** *"What is the difference between exactly-once, at-least-once, and at-most-once delivery?"*
- A) They describe how many consumers can read a message (Incorrect)
- B) They describe delivery guarantees for how many times a message is processed (Correct)
- C) They describe the number of partitions in a Kafka topic (Incorrect)
- D) They only apply to batch pipelines (Incorrect)
- **Explanation:** **At-most-once:** fire and forget, may lose data. **At-least-once:** retries until acknowledged, may create duplicates (most common). **Exactly-once:** each message processed exactly once (hardest — requires idempotent consumers or transactional writes). Kafka supports exactly-once via idempotent producers + transactional consumers. Most pipelines use at-least-once + deduplication downstream.
