import pandas as pd
import numpy as np

def get_exercise():
    base_data = pd.DataFrame({
        "transaction_id": [1, 2, 3, 4, 5, 6],
        "sale_date": ["2024-01-05", "2024-01-05", "2024-01-06", "2024-01-07", "2024-01-08", "2024-01-08"],
        "product_name": ["Widget A", "Gadget B", "Widget A", "Gizmo C", "Gadget B", "Widget A"],
        "category": ["Electronics", "Electronics", "Electronics", "Home", "Electronics", "Electronics"],
        "unit_price": [29.99, 50.00, 29.99, 19.99, 50.00, 29.99],
        "quantity": [2, 1, 3, 5, 2, 1],
        "customer_name": ["Alice Smith", "Bob Jones", "Alice Smith", "Carol White", "Bob Jones", "Dana Brown"],
        "customer_city": ["New York", "Chicago", "New York", "Houston", "Chicago", "Phoenix"],
        "customer_tier": ["gold", "silver", "gold", "bronze", "silver", "platinum"]
    })

    return {
        "title": "Revenue Data Warehouse — Star Schema Design",
        "subtitle": "Dimensional modeling basics, surrogate keys, star schema JOINs, derived metrics, SCD Type 2",
        "description": "A retail company asks: 'Design a star schema data warehouse for our sales data. Build dimension tables, a fact table, compute KPIs, and handle product price changes over time.' This tests dimensional modeling, multi-table JOINs, aggregation KPIs, and Slowly Changing Dimension (SCD) Type 2.",
        "difficulty_level": "entry_to_senior",
        "source_inspiration": "Amazon, Walmart, Instacart · DataLemur (Revenue Analysis), Interview Query",
        "data": base_data,
        "table_name": "raw_sales",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "Use `drop_duplicates()` on the relevant columns, then reset the index and add 1 to create a surrogate key. For testing, output `result = dim_product`.",
        "hint_sql": "Use `DENSE_RANK() OVER (ORDER BY product_name)` to generate incremental integer keys from distinct values. For the test output, just SELECT the dim_product table.",
        "solution_python": """\
df["sale_date"] = pd.to_datetime(df["sale_date"])

dim_product = (
    df[["product_name", "category"]]
    .drop_duplicates()
    .sort_values("product_name")
    .reset_index(drop=True)
)
dim_product.insert(0, "product_id", dim_product.index + 1)

dim_customer = (
    df[["customer_name", "customer_city", "customer_tier"]]
    .drop_duplicates()
    .sort_values("customer_name")
    .reset_index(drop=True)
)
dim_customer.insert(0, "customer_id", dim_customer.index + 1)

result = dim_product
""",
        "solution_sql": """\
SELECT
    DENSE_RANK() OVER (ORDER BY product_name) AS product_id,
    product_name,
    category
FROM (SELECT DISTINCT product_name, category FROM raw_sales) AS distinct_products
ORDER BY product_id;
""",
        "deep_dive": "Dimensional modeling creates clean, reusable lookup tables. Stage 1 demonstrates star schema setup. Real-world systems also need SCD tracking (Stage 4) to handle data changes without overwriting history.",
        "big_o_explanation": "Time: O(N log N) for sorts or densing rank. Space: O(D) where D is distinct records.",
        "mcq_questions": [
            {
                "question": "What are the main components of a star schema?",
                "stage_number": 1,
                "options": [
                    {"label": "A", "text": "One or more staging tables surrounded by raw data tables", "is_correct": False},
                    {"label": "B", "text": "A central fact table connected to multiple denormalized dimension tables via foreign keys", "is_correct": True},
                    {"label": "C", "text": "Multiple fact tables connected to each other in a chain", "is_correct": False},
                    {"label": "D", "text": "A single denormalized table containing everything", "is_correct": False}
                ],
                "explanation": "A star schema's fact table sits at the center, containing numeric measures and foreign keys. Dimension tables radiate outward, providing context. It is optimized for OLAP queries."
            },
            {
                "question": "What is the difference between additive, semi-additive, and non-additive facts?",
                "stage_number": 2,
                "options": [
                    {"label": "A", "text": "They describe how facts can be aggregated across dimensions", "is_correct": True},
                    {"label": "B", "text": "They describe how many dimension tables connect to the fact table", "is_correct": False},
                    {"label": "C", "text": "They describe the size of the fact table", "is_correct": False},
                    {"label": "D", "text": "They are different types of primary keys", "is_correct": False}
                ],
                "explanation": "Additive facts (revenue) can be summed across all dimensions. Semi-additive (account balance) sum across some dimensions but not others like time. Non-additive (prices, ratios) cannot be summed directly."
            },
            {
                "question": "What is the difference between OLTP and OLAP?",
                "stage_number": 3,
                "options": [
                    {"label": "A", "text": "OLTP is for analytics; OLAP is for transactions", "is_correct": False},
                    {"label": "B", "text": "OLTP handles transactional operations (INSERT/UPDATE); OLAP handles analytical queries (aggregations, reporting)", "is_correct": True},
                    {"label": "C", "text": "They are the same thing with different names", "is_correct": False},
                    {"label": "D", "text": "OLAP systems are always slower than OLTP systems", "is_correct": False}
                ],
                "explanation": "OLTP relies on normalized schemas for fast, low-latency writes. OLAP relies on denormalized structures (star schemas) optimized for heavy read aggregations millions of rows deep."
            },
            {
                "question": "What is the Kimball vs Inmon methodology?",
                "stage_number": 4,
                "options": [
                    {"label": "A", "text": "Kimball builds top-down enterprise models; Inmon builds bottom-up dimensional marts", "is_correct": False},
                    {"label": "B", "text": "Kimball builds bottom-up dimensional data marts; Inmon builds a top-down enterprise data warehouse in 3NF first", "is_correct": True},
                    {"label": "C", "text": "They are the same methodology", "is_correct": False},
                    {"label": "D", "text": "Kimball only works with cloud data warehouses", "is_correct": False}
                ],
                "explanation": "Kimball focuses on bottom-up star schema dimensional marts. Inmon advocates for a centralized 3NF enterprise warehouse first. Modern stacks (medallion architecture) often use a mix of both."
            }
        ],
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Build Dimension Tables",
                "scenario": "The analytics team has inherited a single flat denormalized table — `raw_sales`. Extract a `dim_product` table (product_id, product_name, category) and a `dim_customer` table (customer_id, customer_name, customer_city, customer_tier). Assign surrogate integer keys starting from 1. Note: For the test output, return ONLY `dim_product` as the result.",
                "hint": "Use drop_duplicates(), arrange and build integer surrogate keys based on it. For the test output, return ONLY `dim_product` as the result.",
                "data": base_data,
                "evaluation_criteria": [
                    "Surrogate keys start at 1 and are contiguous integers",
                    "drop_duplicates() is scoped to the correct columns only",
                    "Both dimension tables are sorted for deterministic, reproducible key assignment",
                    "Does not include transactional columns"
                ],
                "solution_code": """\
df["sale_date"] = pd.to_datetime(df["sale_date"])

# dim_product
dim_product = (
    df[["product_name", "category"]]
    .drop_duplicates()
    .sort_values("product_name")
    .reset_index(drop=True)
)
dim_product.insert(0, "product_id", dim_product.index + 1)

# dim_customer code not checked in expected_output but shown in interview
dim_customer = (
    df[["customer_name", "customer_city", "customer_tier"]]
    .drop_duplicates()
    .sort_values("customer_name")
    .reset_index(drop=True)
)
dim_customer.insert(0, "customer_id", dim_customer.index + 1)

result = dim_product
""",
                "solution_sql": """\
SELECT
    DENSE_RANK() OVER (ORDER BY product_name) AS product_id,
    product_name,
    category
FROM (SELECT DISTINCT product_name, category FROM raw_sales) AS distinct_products
ORDER BY product_id;
""",
                "expected_output": pd.DataFrame({
                    "product_id": [1, 2, 3],
                    "product_name": ["Gadget B", "Gizmo C", "Widget A"],
                    "category": ["Electronics", "Home", "Electronics"]
                }),
                "big_o_explanation": "**Time:** O(N log N) — dominated by `sort_values()` for deterministic key ordering.\n**Space:** O(D) where D is the number of distinct records.",
                "follow_up_probes": [
                    "Why use surrogate keys instead of natural keys like `product_name`?",
                    "If a customer moves from 'silver' to 'gold' tier, how would you handle that in `dim_customer`?",
                    "What is the difference between a surrogate key and a natural key?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Build Fact Table",
                "scenario": "With dimension tables created, you now need to build the central fact table: `fact_sales`. Join `raw_sales` to `dim_product` and `dim_customer` on name to get their surrogate keys, then compute `total_amount = unit_price × quantity`. The resulting fact table should contain only keys and measures.",
                "hint": "Merge `raw_sales` with `dim_product` on `product_name`, then with `dim_customer` on `customer_name`. Keep only keys and measures. In SQL, use multi-table JOINs and calculate total_amount.",
                "data": base_data,
                "evaluation_criteria": [
                    "Fact table contains only keys and measures",
                    "total_amount is correctly computed as unit_price × quantity",
                    "JOIN is on natural keys",
                    "sale_date is present as a degenerate dimension"
                ],
                "solution_code": """\
df["sale_date"] = pd.to_datetime(df["sale_date"])

dim_product = (
    df[["product_name", "category"]]
    .drop_duplicates()
    .sort_values("product_name")
    .reset_index(drop=True)
)
dim_product.insert(0, "product_id", dim_product.index + 1)

dim_customer = (
    df[["customer_name", "customer_city", "customer_tier"]]
    .drop_duplicates()
    .sort_values("customer_name")
    .reset_index(drop=True)
)
dim_customer.insert(0, "customer_id", dim_customer.index + 1)

fact_sales = df.merge(dim_product[["product_id", "product_name"]], on="product_name")
fact_sales = fact_sales.merge(dim_customer[["customer_id", "customer_name"]], on="customer_name")

fact_sales["total_amount"] = (fact_sales["unit_price"] * fact_sales["quantity"]).round(2)

result = fact_sales[[
    "transaction_id", "sale_date", "product_id", "customer_id",
    "unit_price", "quantity", "total_amount"
]].sort_values("transaction_id").reset_index(drop=True)
""",
                "solution_sql": """\
WITH DimProduct AS (
    SELECT DENSE_RANK() OVER (ORDER BY product_name) AS product_id, product_name
    FROM (SELECT DISTINCT product_name FROM raw_sales) p
),
DimCustomer AS (
    SELECT DENSE_RANK() OVER (ORDER BY customer_name) AS customer_id, customer_name
    FROM (SELECT DISTINCT customer_name FROM raw_sales) c
)
SELECT
    r.transaction_id,
    CAST(r.sale_date AS TIMESTAMP) AS sale_date,
    dp.product_id,
    dc.customer_id,
    r.unit_price,
    r.quantity,
    ROUND(r.unit_price * r.quantity, 2) AS total_amount
FROM raw_sales r
JOIN DimProduct dp ON r.product_name = dp.product_name
JOIN DimCustomer dc ON r.customer_name = dc.customer_name
ORDER BY r.transaction_id;
""",
                "expected_output": pd.DataFrame({
                    "transaction_id": [1, 2, 3, 4, 5, 6],
                    "sale_date": pd.to_datetime(["2024-01-05", "2024-01-05", "2024-01-06", "2024-01-07", "2024-01-08", "2024-01-08"]),
                    "product_id": [3, 1, 3, 2, 1, 3],
                    "customer_id": [1, 2, 1, 3, 2, 4],
                    "unit_price": [29.99, 50.00, 29.99, 19.99, 50.00, 29.99],
                    "quantity": [2, 1, 3, 5, 2, 1],
                    "total_amount": [59.98, 50.00, 89.97, 99.95, 100.00, 29.99]
                }),
                "big_o_explanation": "**Time:** O(N log D) — merging N fact rows with D-sized dimension tables.\n**Space:** O(N) for the output fact table.",
                "follow_up_probes": [
                    "The fact table still contains `unit_price` — is that a dimension attribute or a measure?",
                    "How would you build a `dim_date` table and join it here?",
                    "If two products with the same name but different categories existed, how would your current JOIN logic break?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Calculate Revenue KPIs",
                "scenario": "Using the fact table, compute for each `sale_date`: total revenue (sum of `total_amount`), AOV (Average Order Value = total revenue / number of transactions), and items per order (total quantity / number of transactions). Round monetary and float values to 2 decimal places.",
                "hint": "Use groupby('sale_date') and multiple aggregations. AOV = total revenue / transaction count. In SQL, use SUM and COUNT.",
                "data": pd.DataFrame({
                    "transaction_id": [1, 2, 3, 4, 5, 6],
                    "sale_date": pd.to_datetime(["2024-01-05", "2024-01-05", "2024-01-06", "2024-01-07", "2024-01-08", "2024-01-08"]),
                    "product_id": [3, 1, 3, 2, 1, 3],
                    "customer_id": [1, 2, 1, 3, 2, 4],
                    "unit_price": [29.99, 50.00, 29.99, 19.99, 50.00, 29.99],
                    "quantity": [2, 1, 3, 5, 2, 1],
                    "total_amount": [59.98, 50.00, 89.97, 99.95, 100.00, 29.99]
                }),
                "table_name": "fact_sales",
                "evaluation_criteria": [
                    "AOV is computed as a ratio of aggregates",
                    "items_per_order uses integer quantity",
                    "Monetary columns rounded to 2 decimal places",
                    "num_transactions counts distinct transactions"
                ],
                "solution_code": """\
kpis = df.groupby("sale_date").agg(
    total_revenue=("total_amount", "sum"),
    num_transactions=("transaction_id", "count"),
    total_quantity=("quantity", "sum")
).reset_index()

kpis["aov"] = (kpis["total_revenue"] / kpis["num_transactions"]).round(2)
kpis["items_per_order"] = (kpis["total_quantity"] / kpis["num_transactions"]).astype(float).round(2)
kpis["total_revenue"] = kpis["total_revenue"].round(2)

result = kpis[["sale_date", "total_revenue", "num_transactions", "aov", "items_per_order"]] \\
    .sort_values("sale_date").reset_index(drop=True)
""",
                "solution_sql": """\
SELECT
    CAST(sale_date AS TIMESTAMP) AS sale_date,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    COUNT(*) AS num_transactions,
    ROUND(SUM(total_amount) / COUNT(*), 2) AS aov,
    ROUND(CAST(SUM(quantity) AS DOUBLE) / COUNT(*), 2) AS items_per_order
FROM raw_sales
GROUP BY sale_date
ORDER BY sale_date;
""",
                "expected_output": pd.DataFrame({
                    "sale_date": pd.to_datetime(["2024-01-05", "2024-01-06", "2024-01-07", "2024-01-08"]),
                    "total_revenue": [109.98, 89.97, 99.95, 129.99],
                    "num_transactions": [2, 1, 1, 2],
                    "aov": [54.99, 89.97, 99.95, 65.00],
                    "items_per_order": [1.50, 3.00, 5.00, 1.50]
                }),
                "big_o_explanation": "**Time:** O(N log N) — `groupby` requires processing N fact rows.\n**Space:** O(D_date) for output.",
                "follow_up_probes": [
                    "What does AOV stand for?",
                    "If you wanted weekly AOV instead of daily, how would you change this query?",
                    "Why might AVG(total_amount) give a different answer than SUM(total_amount) / COUNT(*)?"
                ]
            },
            {
                "stage_number": 4,
                "title": "SCD Type 2 for Price Changes",
                "scenario": "Implement SCD Type 2 for product pricing: given a new price update event table, generate an updated `dim_product_prices` table where each row represents a valid price period with `effective_start`, `effective_end` (NULL = still active), and `is_current` flag.",
                "hint": "Sort by product and date. Use shift()/LEAD() to determine effective_end. In SQL, you can mock the unified events table first before LEAD.",
                "data": pd.DataFrame({
                    "product_name": ["Widget A", "Gadget B", "Gizmo C", "Widget A", "Gadget B", "Widget A"],
                    "unit_price": [29.99, 50.00, 19.99, 34.99, 44.99, 39.99],
                    "effective_date": pd.to_datetime([
                        "2024-01-01", "2024-01-01", "2024-01-01",
                        "2024-02-01", "2024-03-01", "2024-03-15"
                    ])
                }),
                "table_name": "all_price_events",
                "evaluation_criteria": [
                    "`effective_end` is correctly set to the *next* event's `effective_start`",
                    "`is_current = True` only for the row with `effective_end IS NULL`",
                    "Handles products with only one price event (Gizmo C)",
                    "Does not confuse SCD Type 2 with SCD Type 1"
                ],
                "solution_code": """\
price_events = df.sort_values(["product_name", "effective_date"]).reset_index(drop=True)

price_events["effective_end"] = price_events.groupby("product_name")["effective_date"].shift(-1)
price_events["is_current"] = price_events["effective_end"].isna()

result = price_events.rename(columns={"effective_date": "effective_start"})[[
    "product_name", "unit_price", "effective_start", "effective_end", "is_current"
]].reset_index(drop=True)
""",
                "solution_sql": """\
WITH WithLead AS (
    SELECT
        product_name,
        unit_price,
        effective_date AS effective_start,
        LEAD(effective_date) OVER (PARTITION BY product_name ORDER BY effective_date) AS effective_end
    FROM raw_sales
)
SELECT
    product_name,
    unit_price,
    CAST(effective_start AS TIMESTAMP) AS effective_start,
    CAST(effective_end AS TIMESTAMP) AS effective_end,
    CASE WHEN effective_end IS NULL THEN TRUE ELSE FALSE END AS is_current
FROM WithLead
ORDER BY product_name, effective_start;
""",
                "expected_output": pd.DataFrame({
                    "product_name": ["Gadget B", "Gadget B", "Gizmo C", "Widget A", "Widget A", "Widget A"],
                    "unit_price": [50.00, 44.99, 19.99, 29.99, 34.99, 39.99],
                    "effective_start": pd.to_datetime(["2024-01-01", "2024-03-01", "2024-01-01", "2024-01-01", "2024-02-01", "2024-03-15"]),
                    "effective_end": pd.to_datetime(["2024-03-01", "NaT", "NaT", "2024-02-01", "2024-03-15", "NaT"]),
                    "is_current": [False, True, True, False, False, True]
                }),
                "big_o_explanation": "**Time:** O(N log N) — sort by (product_name, effective_date) dominates.\n**Space:** O(N) — one output row per price event.",
                "follow_up_probes": [
                    "How would you query this SCD Type 2 table to find the price of Widget A on 2024-02-15?",
                    "What's the difference between SCD Type 1, Type 2, and Type 3?",
                    "If you receive a price update that's *backdated*, how would you handle it?"
                ]
            }
        ]
    }
