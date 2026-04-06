import pandas as pd

def get_exercise():
    base_data = pd.DataFrame({
        "event_id": ["E001", "E002", "E001", "E003", "E002"],
        "order_id": [1001, 1002, 1001, 1003, 1002],
        "customer_id": [201, 202, 201, 203, 202],
        "product_id": [301, 302, 301, 303, 302],
        "order_status": ["placed", "placed", "placed", "placed", "placed"],
        "amount": [49.99, 29.99, 49.99, 99.99, 29.99],
        "event_timestamp": [
            "2024-01-15 10:00:00", 
            "2024-01-15 10:05:00", 
            "2024-01-15 10:00:00", 
            "2024-01-15 10:10:00", 
            "2024-01-15 10:05:00"
        ]
    })

    return {
        "title": "E-Commerce Order Pipeline — Batch vs Stream",
        "subtitle": "Deduplication, JOINs, Dimensional Modeling, Late-Arriving Data",
        "description": "An e-commerce company processes millions of orders daily. The data engineering team must build a pipeline that deduplicates raw order events, builds fact/dimension tables for analytics, and handles late-arriving data and order status changes. \"Should this be a streaming pipeline or a batch pipeline? How would you handle duplicate events and late-arriving data?\"",
        "difficulty_level": "entry_to_senior",
        "source_inspiration": "Amazon, Stripe, Shopify · StrataScratch, Interview Query",
        "data": base_data,
        "table_name": "raw_order_events",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "In Python, use `drop_duplicates()` on the event_id column.",
        "hint_sql": "In SQL, use `DISTINCT` or `GROUP BY` with `MIN()` on columns to remove duplicated events.",
        "solution_python": """\
result = df.drop_duplicates(subset=["event_id"]).sort_values("event_id").reset_index(drop=True)
""",
        "solution_sql": """\
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
""",
        "deep_dive": "Handling duplicate stream events requires processing distinct unique identifiers. Later stages involve dealing with mutable statuses and upserts to avoid double-counting.",
        "big_o_explanation": "Time Complexity: O(N log N) for sort-based DISTINCT filtering. Space Complexity: O(N) since output requires keeping copies of unique valid events.",
        "mcq_questions": [
            {
                "question": "When should you use a streaming pipeline instead of a batch pipeline?",
                "stage_number": 1,
                "options": [
                    {"label": "A", "text": "Always \u2014 streaming is strictly better than batch", "is_correct": False},
                    {"label": "B", "text": "When data needs to be processed within seconds/minutes of arrival for real-time decisions", "is_correct": True},
                    {"label": "C", "text": "When you have very large historical datasets to process", "is_correct": False},
                    {"label": "D", "text": "When you want to minimise infrastructure costs", "is_correct": False}
                ],
                "explanation": "Streaming pipelines (Kafka, Flink, Spark Structured Streaming) are essential when low latency matters \u2014 fraud detection, live dashboards, real-time recommendations. Batch pipelines (Airflow + Spark, dbt) are cheaper, simpler, and better for historical analysis, nightly ETL, and compliance reports where hours of latency are acceptable. Most production systems use a hybrid (Lambda/Kappa architecture)."
            },
            {
                "question": "What does 'idempotency' mean in data pipelines?",
                "stage_number": 2,
                "options": [
                    {"label": "A", "text": "A pipeline that runs exactly once and never retries", "is_correct": False},
                    {"label": "B", "text": "A pipeline that produces the same result regardless of how many times it runs on the same input", "is_correct": True},
                    {"label": "C", "text": "A pipeline that deletes old data before writing new data", "is_correct": False},
                    {"label": "D", "text": "A pipeline that runs in parallel across multiple nodes", "is_correct": False}
                ],
                "explanation": "Idempotent pipelines are safe to retry. If a job fails halfway and reruns, it won't create duplicates or corrupt data. Techniques include: UPSERT/MERGE instead of INSERT, writing to partitioned staging tables then atomically swapping, and using INSERT ... ON CONFLICT DO UPDATE. This is critical for exactly-once semantics in streaming AND batch."
            },
            {
                "question": "What is the difference between event-time and processing-time?",
                "stage_number": 3,
                "options": [
                    {"label": "A", "text": "Event-time is when the system processes the data; processing-time is when the event occurred", "is_correct": False},
                    {"label": "B", "text": "Event-time is when the event occurred; processing-time is when the system processes the data", "is_correct": True},
                    {"label": "C", "text": "They are the same thing in batch pipelines", "is_correct": False},
                    {"label": "D", "text": "Event-time only matters in batch systems", "is_correct": False}
                ],
                "explanation": "In streaming, events can arrive out of order or late. A payment at 14:00:00 (event-time) might reach your pipeline at 14:05:00 (processing-time). If you window/aggregate by processing-time, results are non-deterministic. Production systems use event-time with watermarks to handle late data (e.g., \"wait 5 minutes for stragglers before closing the window\")."
            },
            {
                "question": "What is the difference between exactly-once, at-least-once, and at-most-once delivery?",
                "stage_number": 4,
                "options": [
                    {"label": "A", "text": "They describe how many consumers can read a message", "is_correct": False},
                    {"label": "B", "text": "They describe delivery guarantees for how many times a message is processed", "is_correct": True},
                    {"label": "C", "text": "They describe the number of partitions in a Kafka topic", "is_correct": False},
                    {"label": "D", "text": "They only apply to batch pipelines", "is_correct": False}
                ],
                "explanation": "At-most-once: fire and forget, may lose data. At-least-once: retries until acknowledged, may create duplicates (most common). Exactly-once: each message processed exactly once (hardest \u2014 requires idempotent consumers or transactional writes). Kafka supports exactly-once via idempotent producers + transactional consumers. Most pipelines use at-least-once + deduplication downstream."
            }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Deduplicate Order Events",
                "scenario": "Our upstream order service sometimes emits the same event twice due to retry logic. Before we can do any analysis, we need to remove exact-duplicate events. Deduplicate the raw_order_events data by event_id, keeping only one copy of each event.",
                "hint": "In Python, use drop_duplicates() on the event_id column. In SQL, use DISTINCT or a GROUP BY on event_id.",
                "data": base_data,
                "evaluation_criteria": [
                    "Correctly identifies event_id as the deduplication key",
                    "Understands that exact duplicates share all column values",
                    "Chooses an efficient deduplication method"
                ],
                "solution_code": """\
result = df.drop_duplicates(subset=["event_id"]).sort_values("event_id").reset_index(drop=True)
""",
                "solution_sql": """\
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
""",
                "expected_output": pd.DataFrame({
                    "event_id": ["E001", "E002", "E003"],
                    "order_id": [1001, 1002, 1003],
                    "customer_id": [201, 202, 203],
                    "product_id": [301, 302, 303],
                    "order_status": ["placed", "placed", "placed"],
                    "amount": [49.99, 29.99, 99.99],
                    "event_timestamp": ["2024-01-15 10:00:00", "2024-01-15 10:05:00", "2024-01-15 10:10:00"]
                }),
                "big_o_explanation": "**Time:** O(N) for hash-based deduplication in Python; O(N log N) if SQL uses sort-based DISTINCT\n**Space:** O(N) to store the hash set of seen event IDs",
                "follow_up_probes": [
                    "What if duplicates had slightly different timestamps (e.g., due to clock skew)? Would this approach still work?",
                    "How would you handle deduplication at scale \u2014 millions of events per hour?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Latest Status Per Order",
                "scenario": "Each order goes through multiple status transitions: placed -> confirmed -> shipped -> delivered (or cancelled). The source table has one row per status change event. We need to find the current (most recent) status for each order.",
                "hint": "In Python, sort by timestamp and drop duplicates on order_id keeping the last. In SQL, use ROW_NUMBER() partitioned by order_id, ordered by event_timestamp DESC.",
                "data": pd.DataFrame({
                    "event_id": ["E001", "E004", "E007", "E002", "E005", "E003", "E006"],
                    "order_id": [1001, 1001, 1001, 1002, 1002, 1003, 1003],
                    "customer_id": [201, 201, 201, 202, 202, 203, 203],
                    "product_id": [301, 301, 301, 302, 302, 303, 303],
                    "order_status": ["placed", "confirmed", "shipped", "placed", "confirmed", "placed", "cancelled"],
                    "amount": [49.99, 49.99, 49.99, 29.99, 29.99, 99.99, 99.99],
                    "event_timestamp": [
                        "2024-01-15 10:00:00",
                        "2024-01-15 12:00:00",
                        "2024-01-16 09:00:00",
                        "2024-01-15 10:05:00",
                        "2024-01-15 14:00:00",
                        "2024-01-15 10:10:00",
                        "2024-01-15 16:00:00"
                    ]
                }),
                "evaluation_criteria": [
                    "Recognizes the need to sort by timestamp before deduplicating",
                    "Correctly uses keep='last' (Python) or DESC ordering (SQL) to retain the most recent event",
                    "Partitions correctly by order_id"
                ],
                "solution_code": """\
df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
result = df.sort_values("event_timestamp").drop_duplicates(subset=["order_id"], keep="last")
result = result.sort_values("order_id").reset_index(drop=True)
""",
                "solution_sql": """\
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
""",
                "expected_output": pd.DataFrame({
                    "event_id": ["E007", "E005", "E006"],
                    "order_id": [1001, 1002, 1003],
                    "customer_id": [201, 202, 203],
                    "product_id": [301, 302, 303],
                    "order_status": ["shipped", "confirmed", "cancelled"],
                    "amount": [49.99, 29.99, 99.99],
                    "event_timestamp": pd.to_datetime([
                        "2024-01-16 09:00:00", "2024-01-15 14:00:00", "2024-01-15 16:00:00"
                    ])
                }),
                "big_o_explanation": "**Time:** O(N log N) \u2014 sorting by timestamp dominates\n**Space:** O(N) to hold the sorted intermediate result and partition state",
                "follow_up_probes": [
                    "Why is ROW_NUMBER() preferred over RANK() here?",
                    "What if two status events for the same order have the exact same timestamp?",
                    "How does this pattern relate to Slowly Changing Dimensions (SCD Type 1)?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Build Fact Table",
                "scenario": "Now that we have the latest status per order, we need to join the orders with product and customer dimension tables to build a fact_orders table. Calculate the total revenue per customer.",
                "hint": "In Python, use pd.merge() to join the tables, then groupby() to aggregate. In SQL, use JOIN and GROUP BY.",
                "data": pd.DataFrame({
                    "order_id": [1001, 1002, 1003, 1004, 1005],
                    "customer_id": [201, 202, 201, 203, 202],
                    "product_id": [301, 302, 303, 301, 304],
                    "order_status": ["delivered", "delivered", "delivered", "cancelled", "delivered"],
                    "amount": [49.99, 29.99, 99.99, 49.99, 19.99],
                    "event_timestamp": [
                        "2024-01-16 15:00:00",
                        "2024-01-17 12:00:00",
                        "2024-01-17 14:00:00",
                        "2024-01-18 09:00:00",
                        "2024-01-18 11:00:00"
                    ]
                }),
                "evaluation_criteria": [
                    "Correctly filters out non-delivered orders before aggregation",
                    "Performs JOINs on the correct foreign keys",
                    "Aggregates revenue at the right grain (per customer)",
                    "Understands why cancelled orders should be excluded from revenue calculations"
                ],
                "solution_code": """\
# Setup mock dimension tables
customers_df = pd.DataFrame({
    "customer_id": [201, 202, 203],
    "customer_name": ["Alice", "Bob", "Charlie"],
    "customer_city": ["New York", "San Francisco", "Chicago"],
    "customer_tier": ["gold", "silver", "bronze"]
})
products_df = pd.DataFrame({
    "product_id": [301, 302, 303, 304],
    "product_name": ["Wireless Mouse", "Python Book", "Standing Desk", "USB Cable"],
    "category": ["Electronics", "Books", "Furniture", "Electronics"]
})

# Filter to only delivered orders
delivered = df[df["order_status"] == "delivered"].copy()

# Join with dimensions
fact = delivered.merge(customers_df, on="customer_id").merge(products_df, on="product_id")

# Compute total revenue per customer
result = fact.groupby(
    ["customer_id", "customer_name", "customer_city", "customer_tier"],
    as_index=False
)["amount"].sum()
result = result.rename(columns={"amount": "total_revenue"})
result = result.sort_values("customer_id").reset_index(drop=True)
""",
                "solution_sql": """\
WITH dim_customer AS (
    SELECT 201 AS customer_id, 'Alice' AS customer_name, 'New York' AS customer_city, 'gold' AS customer_tier UNION ALL
    SELECT 202, 'Bob', 'San Francisco', 'silver' UNION ALL
    SELECT 203, 'Charlie', 'Chicago', 'bronze'
),
dim_product AS (
    SELECT 301 AS product_id, 'Wireless Mouse' AS product_name, 'Electronics' AS category UNION ALL
    SELECT 302, 'Python Book', 'Books' UNION ALL
    SELECT 303, 'Standing Desk', 'Furniture' UNION ALL
    SELECT 304, 'USB Cable', 'Electronics'
)
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
""",
                "expected_output": pd.DataFrame({
                    "customer_id": [201, 202],
                    "customer_name": ["Alice", "Bob"],
                    "customer_city": ["New York", "San Francisco"],
                    "customer_tier": ["gold", "silver"],
                    "total_revenue": [149.98, 49.98]
                }),
                "big_o_explanation": "**Time:** O(N × M) for nested-loop JOINs, O(N + M) for hash JOINs in optimized engines, plus O(K) for aggregation (K = output groups)\n**Space:** O(N + M) for hash tables built during joins",
                "follow_up_probes": [
                    "Why filter by order_status = 'delivered' rather than including all orders?",
                    "What is the grain of this fact table?",
                    "How would you handle a customer with zero delivered orders?"
                ]
            },
            {
                "stage_number": 4,
                "title": "Handle Late-Arriving Data",
                "scenario": "In production, events don't always arrive in order. A \"delivered\" event might arrive before the \"shipped\" event due to network delays. Implement an upsert strategy: given an existing current_orders snapshot and a batch of new incoming_events, update each order's status ONLY if the incoming event is more recent (by event_timestamp) than what's already stored. This ensures idempotent, out-of-order-safe updates.",
                "hint": "In Python, concatenate the existing and incoming data, then keep the row with the latest timestamp per order_id. In SQL, use MERGE or an analytical function representing the final combined view.",
                "data": pd.DataFrame({
                    "order_id": [1001, 1002, 1003],
                    "customer_id": [201, 202, 203],
                    "order_status": ["confirmed", "placed", "placed"],
                    "amount": [49.99, 29.99, 99.99],
                    "event_timestamp": [
                        "2024-01-15 12:00:00",
                        "2024-01-15 10:05:00",
                        "2024-01-15 10:10:00"
                    ]
                }),
                "evaluation_criteria": [
                    "Implements timestamp-aware upsert \u2014 rejects stale incoming events",
                    "Handles new orders (INSERT path) correctly",
                    "Result is idempotent \u2014 re-running with the same incoming events produces the same output",
                    "Understands why this matters for late-arriving/out-of-order data in production"
                ],
                "solution_code": """\
# Mocking incoming_events dataframe
incoming_events = pd.DataFrame({
    "order_id": [1001, 1002, 1003, 1004],
    "customer_id": [201, 202, 203, 204],
    "order_status": ["shipped", "confirmed", "placed", "placed"],
    "amount": [49.99, 29.99, 99.99, 19.99],
    "event_timestamp": [
        "2024-01-16 09:00:00",
        "2024-01-15 14:00:00",
        "2024-01-15 08:00:00",
        "2024-01-16 10:00:00"
    ]
})

current_df = df.copy()
current_df["event_timestamp"] = pd.to_datetime(current_df["event_timestamp"])
incoming_df = incoming_events.copy()
incoming_df["event_timestamp"] = pd.to_datetime(incoming_df["event_timestamp"])

# Concatenate current state with incoming events
combined = pd.concat([current_df, incoming_df], ignore_index=True)

# Keep the row with the latest timestamp per order (upsert logic)
combined = combined.sort_values("event_timestamp")
result = combined.drop_duplicates(subset=["order_id"], keep="last")
result = result.sort_values("order_id").reset_index(drop=True)
""",
                "solution_sql": """\
WITH incoming_events AS (
    SELECT 1001 AS order_id, 201 AS customer_id, 'shipped' AS order_status, 49.99 AS amount, '2024-01-16 09:00:00' AS event_timestamp UNION ALL
    SELECT 1002, 202, 'confirmed', 29.99, '2024-01-15 14:00:00' UNION ALL
    SELECT 1003, 203, 'placed', 99.99, '2024-01-15 08:00:00' UNION ALL
    SELECT 1004, 204, 'placed', 19.99, '2024-01-16 10:00:00'
),
CombinedEvents AS (
    SELECT order_id, customer_id, order_status, amount, CAST(event_timestamp AS TIMESTAMP) as event_timestamp
    FROM raw_order_events
    UNION ALL
    SELECT order_id, customer_id, order_status, amount, CAST(event_timestamp AS TIMESTAMP) as event_timestamp
    FROM incoming_events
),
RankedEvents AS (
    SELECT
        order_id,
        customer_id,
        order_status,
        amount,
        event_timestamp,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY event_timestamp DESC) AS rn
    FROM CombinedEvents
)
SELECT order_id, customer_id, order_status, amount, event_timestamp
FROM RankedEvents
WHERE rn = 1
ORDER BY order_id;
""",
                "expected_output": pd.DataFrame({
                    "order_id": [1001, 1002, 1003, 1004],
                    "customer_id": [201, 202, 203, 204],
                    "order_status": ["shipped", "confirmed", "placed", "placed"],
                    "amount": [49.99, 29.99, 99.99, 19.99],
                    "event_timestamp": pd.to_datetime([
                        "2024-01-16 09:00:00",
                        "2024-01-15 14:00:00",
                        "2024-01-15 10:10:00",
                        "2024-01-16 10:00:00"
                    ])
                }),
                "big_o_explanation": "**Time:** O(N + M) for hash-based merge, O((N + M) log (N + M)) if sort-based deduplication is used\n**Space:** O(N + M) for the combined dataset",
                "follow_up_probes": [
                    "Why is the timestamp guard (source.timestamp > target.timestamp) critical?",
                    "What would happen if you ran this merge job twice with the same incoming data?",
                    "How does this relate to exactly-once vs at-least-once delivery guarantees?",
                    "In a real streaming system, how would watermarks help with this problem?"
                ]
            }
        ]
    }
