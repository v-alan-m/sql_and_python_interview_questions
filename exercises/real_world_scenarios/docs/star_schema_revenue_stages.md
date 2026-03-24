# Scenario 5: Revenue Data Warehouse — Star Schema Design

**Source Inspiration:** Amazon, Walmart, Instacart · DataLemur (Revenue Analysis), Interview Query
**Level Range:** Entry → Senior
**Description:** A retail company asks: *"Design a star schema data warehouse for our sales data. Build dimension tables, a fact table, compute KPIs, and handle product price changes over time."* This is THE classic data modeling interview question that spans entry through senior — testing dimensional modeling, multi-table JOIN design, aggregation KPIs, and Slowly Changing Dimension (SCD) Type 2.
**Reuses Patterns From:** `exercises/sql_and_pandas/cumulative_revenue.py`, `exercises/sql_and_pandas/daily_price_delta.py`

## Data Schema (`raw_sales`)
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

---
## Stages

### Stage 1: Build Dimension Tables
**Level:** Entry
**Key Concepts:** Dimensional modeling basics, surrogate key generation, `factorize()`, `drop_duplicates()`, `DENSE_RANK()`
**Scenario:** The analytics team has inherited a single flat denormalized table — `raw_sales` — that contains product and customer attributes repeated on every row. Your first task is to normalize this into reusable dimension tables. Extract a `dim_product` table (with columns: `product_id`, `product_name`, `category`) and a `dim_customer` table (with columns: `customer_id`, `customer_name`, `customer_city`, `customer_tier`). Assign surrogate integer keys starting from 1.
**Coding Task:** Extract `dim_product` and `dim_customer` from raw data with surrogate keys.

**Hint:** Use `drop_duplicates()` on the relevant columns, then reset the index and add 1 to create a surrogate key (or use `pd.factorize()`). In SQL, use `DENSE_RANK() OVER (ORDER BY product_name)` to generate incremental integer keys from distinct values.

**Sample Data:**
```
transaction_id | sale_date  | product_name    | category    | unit_price | quantity | customer_name | customer_city | customer_tier
1              | 2024-01-05 | Widget A        | Electronics | 29.99      | 2        | Alice Smith   | New York      | gold
2              | 2024-01-05 | Gadget B        | Electronics | 49.99      | 1        | Bob Jones     | Chicago       | silver
3              | 2024-01-06 | Widget A        | Electronics | 29.99      | 3        | Alice Smith   | New York      | gold
4              | 2024-01-07 | Gizmo C         | Home        | 19.99      | 5        | Carol White   | Houston       | bronze
5              | 2024-01-08 | Gadget B        | Electronics | 49.99      | 2        | Bob Jones     | Chicago       | silver
6              | 2024-01-08 | Widget A        | Electronics | 29.99      | 1        | Dana Brown    | Phoenix       | platinum
```

**Python Solution:**
```python
df["sale_date"] = pd.to_datetime(df["sale_date"])

# dim_product
dim_product = (
    df[["product_name", "category"]]
    .drop_duplicates()
    .sort_values("product_name")
    .reset_index(drop=True)
)
dim_product.insert(0, "product_id", dim_product.index + 1)

# dim_customer
dim_customer = (
    df[["customer_name", "customer_city", "customer_tier"]]
    .drop_duplicates()
    .sort_values("customer_name")
    .reset_index(drop=True)
)
dim_customer.insert(0, "customer_id", dim_customer.index + 1)
```

**SQL Solution:**
```sql
-- dim_product
SELECT
    DENSE_RANK() OVER (ORDER BY product_name) AS product_id,
    product_name,
    category
FROM (SELECT DISTINCT product_name, category FROM raw_sales) AS distinct_products
ORDER BY product_id;

-- dim_customer
SELECT
    DENSE_RANK() OVER (ORDER BY customer_name) AS customer_id,
    customer_name,
    customer_city,
    customer_tier
FROM (SELECT DISTINCT customer_name, customer_city, customer_tier FROM raw_sales) AS distinct_customers
ORDER BY customer_id;
```

**Expected Output — dim_product:**
```
product_id | product_name | category
1          | Gadget B     | Electronics
2          | Gizmo C      | Home
3          | Widget A     | Electronics
```

**Expected Output — dim_customer:**
```
customer_id | customer_name | customer_city | customer_tier
1           | Alice Smith   | New York      | gold
2           | Bob Jones     | Chicago       | silver
3           | Carol White   | Houston       | bronze
4           | Dana Brown    | Phoenix       | platinum
```

**Big-O Analysis:**
- **Time:** O(N log N) — dominated by `sort_values()` for deterministic key ordering; `drop_duplicates()` is O(N)
- **Space:** O(D) where D is the number of distinct products/customers — far smaller than N for large fact tables

**Evaluation Criteria:**
- Surrogate keys start at 1 and are contiguous integers (not row indices or hashes)
- `drop_duplicates()` is scoped to the correct columns only (not all columns)
- Both dimension tables are sorted for deterministic, reproducible key assignment
- Does not include transactional columns (`unit_price`, `quantity`, `sale_date`) in dimension tables

**Follow-Up Probes:**
- "Why use surrogate keys instead of natural keys like `product_name`? What problems do natural keys cause?"
- "If a customer moves from 'silver' to 'gold' tier, how would you handle that in `dim_customer`?"
- "What is the difference between a surrogate key and a natural key? Which does Kimball methodology recommend?"

---
### Stage 2: Build Fact Table
**Level:** Mid
**Key Concepts:** Star schema JOINs, fact table construction, `total_amount` derived metric, referential integrity
**Scenario:** With dimension tables created, you now need to build the central fact table: `fact_sales`. Join `raw_sales` to `dim_product` and `dim_customer` on name to get their surrogate keys, then compute `total_amount = unit_price × quantity`. The resulting fact table should contain only **keys and measures** — no descriptive attributes (those live in the dimensions).
**Coding Task:** Create `fact_sales` by joining dimensions, compute `total_amount`.

**Hint:** Merge `raw_sales` with `dim_product` on `product_name`, then with `dim_customer` on `customer_name`. Keep only `transaction_id`, `sale_date`, `product_id`, `customer_id`, `unit_price`, `quantity`, and `total_amount`. In SQL, use a multi-table JOIN, then compute `unit_price * quantity AS total_amount`.

**Sample Data:** (same `raw_sales` as Stage 1, plus the dimension tables from Stage 1 output)

**Python Solution:**
```python
df["sale_date"] = pd.to_datetime(df["sale_date"])

# Rebuild dimensions (same logic as Stage 1)
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

# Build fact table
fact_sales = df.merge(dim_product[["product_id", "product_name"]], on="product_name")
fact_sales = fact_sales.merge(dim_customer[["customer_id", "customer_name"]], on="customer_name")

fact_sales["total_amount"] = (fact_sales["unit_price"] * fact_sales["quantity"]).round(2)

result = fact_sales[[
    "transaction_id", "sale_date", "product_id", "customer_id",
    "unit_price", "quantity", "total_amount"
]].sort_values("transaction_id").reset_index(drop=True)
```

**SQL Solution:**
```sql
WITH DimProduct AS (
    SELECT
        DENSE_RANK() OVER (ORDER BY product_name) AS product_id,
        product_name
    FROM (SELECT DISTINCT product_name FROM raw_sales) p
),
DimCustomer AS (
    SELECT
        DENSE_RANK() OVER (ORDER BY customer_name) AS customer_id,
        customer_name
    FROM (SELECT DISTINCT customer_name FROM raw_sales) c
)
SELECT
    r.transaction_id,
    r.sale_date,
    dp.product_id,
    dc.customer_id,
    r.unit_price,
    r.quantity,
    ROUND(r.unit_price * r.quantity, 2) AS total_amount
FROM raw_sales r
JOIN DimProduct   dp ON r.product_name   = dp.product_name
JOIN DimCustomer  dc ON r.customer_name  = dc.customer_name
ORDER BY r.transaction_id;
```

**Expected Output — fact_sales:**
```
transaction_id | sale_date  | product_id | customer_id | unit_price | quantity | total_amount
1              | 2024-01-05 | 3          | 1           | 29.99      | 2        | 59.98
2              | 2024-01-05 | 1          | 2           | 49.99      | 1        | 49.99
3              | 2024-01-06 | 3          | 1           | 29.99      | 3        | 89.97
4              | 2024-01-07 | 2          | 3           | 19.99      | 5        | 99.95
5              | 2024-01-08 | 1          | 2           | 49.99      | 2        | 99.98
6              | 2024-01-08 | 3          | 4           | 29.99      | 1        | 29.99
```

**Big-O Analysis:**
- **Time:** O(N log D) — merging N fact rows with D-sized dimension tables; hash join would be O(N + D)
- **Space:** O(N) for the output fact table; intermediate merge results are O(N) with proper pandas merge implementation

**Evaluation Criteria:**
- Fact table contains only keys and measures — no descriptive attributes like `product_name` or `customer_city`
- `total_amount` is correctly computed as `unit_price × quantity` (not `unit_price + quantity`)
- JOIN is on natural keys (`product_name`, `customer_name`), not on raw row index
- `sale_date` is present as a degenerate dimension (FK to an implicit `dim_date`, common in star schemas)

**Follow-Up Probes:**
- "The fact table still contains `unit_price` — is that a dimension attribute or a measure? What type of fact is it (additive/semi/non-additive)?"
- "How would you build a `dim_date` table and join it here? What attributes would it have?"
- "If two products with the same name but different categories existed, how would your current JOIN logic break?"

---
### Stage 3: Calculate Revenue KPIs
**Level:** Mid
**Key Concepts:** Multi-metric daily aggregation, AOV (Average Order Value), items per order, `groupby().agg()`
**Scenario:** The finance team wants a daily revenue summary for the dashboard. Using the fact table from Stage 2, compute for each `sale_date`: **total revenue** (sum of `total_amount`), **AOV** (average order value = total revenue / number of transactions), and **items per order** (total quantity / number of transactions). Round monetary values to 2 decimal places. Sort by `sale_date` ascending.
**Coding Task:** Compute total revenue, AOV, and items per order by date.

**Hint:** Use `groupby("sale_date").agg(...)` with named aggregations. AOV = `total_amount.sum() / count of transactions`. Items per order = `quantity.sum() / count of transactions`. In SQL, use `SUM()`, `COUNT()`, and division to compute the derived KPIs in a single `GROUP BY` query.

**Sample Data:** (use the `fact_sales` DataFrame output from Stage 2 — 6 rows, 4 sale dates)

**Python Solution:**
```python
# Build fact_sales (same as Stage 2 — abbreviated here)
df["sale_date"] = pd.to_datetime(df["sale_date"])
df["total_amount"] = (df["unit_price"] * df["quantity"]).round(2)

kpis = df.groupby("sale_date").agg(
    total_revenue=("total_amount", "sum"),
    num_transactions=("transaction_id", "count"),
    total_quantity=("quantity", "sum")
).reset_index()

kpis["aov"] = (kpis["total_revenue"] / kpis["num_transactions"]).round(2)
kpis["items_per_order"] = (kpis["total_quantity"] / kpis["num_transactions"]).round(2)
kpis["total_revenue"] = kpis["total_revenue"].round(2)

result = kpis[["sale_date", "total_revenue", "num_transactions", "aov", "items_per_order"]] \
    .sort_values("sale_date").reset_index(drop=True)
```

**SQL Solution:**
```sql
SELECT
    sale_date,
    ROUND(SUM(total_amount), 2)                        AS total_revenue,
    COUNT(*)                                            AS num_transactions,
    ROUND(SUM(total_amount) / COUNT(*), 2)             AS aov,
    ROUND(SUM(quantity)::NUMERIC / COUNT(*), 2)        AS items_per_order
FROM fact_sales
GROUP BY sale_date
ORDER BY sale_date;
```

**Expected Output:**
```
sale_date  | total_revenue | num_transactions | aov   | items_per_order
2024-01-05 | 109.97        | 2                | 54.99 | 1.50
2024-01-06 | 89.97         | 1                | 89.97 | 3.00
2024-01-07 | 99.95         | 1                | 99.95 | 5.00
2024-01-08 | 129.97        | 2                | 64.99 | 1.50
```

**Big-O Analysis:**
- **Time:** O(N log N) — `groupby` requires a sort-or-hash step over N fact rows; aggregation itself is O(N)
- **Space:** O(D_date) where D_date is the number of distinct sale dates — the output is a tiny summary table

**Evaluation Criteria:**
- AOV is computed as a ratio of aggregates (not an average of individual `total_amount` values — these can differ subtly in edge cases)
- `items_per_order` uses integer `quantity`, not `total_amount`
- Monetary columns rounded to 2 decimal places; `items_per_order` may be a float (e.g., 1.5 items is valid)
- `num_transactions` counts distinct transactions, not product lines

**Follow-Up Probes:**
- "What does AOV stand for and how do companies use it in conjunction with LTV (Lifetime Value)?"
- "If you wanted weekly AOV instead of daily, how would you change this query? What about rolling 7-day AOV?"
- "Why might `AVG(total_amount)` give a different answer than `SUM(total_amount) / COUNT(*)`? When are they identical?"

---
### Stage 4: SCD Type 2 for Price Changes
**Level:** Senior
**Key Concepts:** Slowly Changing Dimensions, `effective_start`, `effective_end`, `is_current`, insert-new-row history tracking, `LAG()` change detection
**Scenario:** The pricing team has updated prices on some products. The data warehouse must preserve the full price history so analysts can answer: *"What was the price of Widget A in January vs March?"* Implement **SCD Type 2** for product pricing: given a new price update event table, generate an updated `dim_product_prices` table where each row represents a valid price period with `effective_start`, `effective_end` (NULL = still active), and `is_current` flag. New prices close the previous row (`effective_end = new_effective_start`) and open a new row.
**Coding Task:** Track historical product prices with `effective_start`, `effective_end`, `is_current`.

**Hint:** Sort all price events by `(product_name, effective_date)`. Use `shift()` within each product group to detect price changes. For each new price, set the previous row's `effective_end` to the new row's `effective_date`. The last row per product always has `effective_end = None` and `is_current = True`. In SQL, use `LEAD()` to look ahead at the next effective date.

**Sample Data:**
```
-- Initial prices (loaded from Stage 1 data)
product_name  | unit_price | effective_date
Widget A      | 29.99      | 2024-01-01
Gadget B      | 49.99      | 2024-01-01
Gizmo C       | 19.99      | 2024-01-01

-- Price update events (arriving later)
product_name  | unit_price | effective_date
Widget A      | 34.99      | 2024-02-01
Gadget B      | 44.99      | 2024-03-01
Widget A      | 39.99      | 2024-03-15
```

**Python Solution:**
```python
import numpy as np

# Combine initial prices + updates
price_events = pd.DataFrame({
    "product_name":   ["Widget A", "Gadget B", "Gizmo C",
                        "Widget A", "Gadget B", "Widget A"],
    "unit_price":     [29.99, 49.99, 19.99, 34.99, 44.99, 39.99],
    "effective_date": pd.to_datetime([
        "2024-01-01", "2024-01-01", "2024-01-01",
        "2024-02-01", "2024-03-01", "2024-03-15"
    ])
})

# Sort by product and effective date to establish chronological order
price_events = price_events.sort_values(
    ["product_name", "effective_date"]
).reset_index(drop=True)

# Use LEAD equivalent: for each row, effective_end = next row's effective_date (within same product)
price_events["effective_end"] = price_events.groupby("product_name")[
    "effective_date"
].shift(-1)

# is_current = True only for the latest row per product (effective_end is NaT)
price_events["is_current"] = price_events["effective_end"].isna()

# Rename for clarity
result = price_events.rename(columns={"effective_date": "effective_start"})[[
    "product_name", "unit_price", "effective_start", "effective_end", "is_current"
]].reset_index(drop=True)
```

**SQL Solution:**
```sql
WITH AllPriceEvents AS (
    -- Union initial prices and updates into one stream
    SELECT product_name, unit_price, '2024-01-01'::DATE AS effective_date FROM dim_product_initial
    UNION ALL
    SELECT product_name, unit_price, effective_date FROM price_updates
),
WithLead AS (
    SELECT
        product_name,
        unit_price,
        effective_date                                         AS effective_start,
        LEAD(effective_date) OVER (
            PARTITION BY product_name
            ORDER BY effective_date
        )                                                      AS effective_end
    FROM AllPriceEvents
)
SELECT
    product_name,
    unit_price,
    effective_start,
    effective_end,
    CASE WHEN effective_end IS NULL THEN TRUE ELSE FALSE END AS is_current
FROM WithLead
ORDER BY product_name, effective_start;
```

**Expected Output — dim_product_prices:**
```
product_name | unit_price | effective_start | effective_end | is_current
Gadget B     | 49.99      | 2024-01-01      | 2024-03-01    | False
Gadget B     | 44.99      | 2024-03-01      | NULL          | True
Gizmo C      | 19.99      | 2024-01-01      | NULL          | True
Widget A     | 29.99      | 2024-01-01      | 2024-02-01    | False
Widget A     | 34.99      | 2024-02-01      | 2024-03-15    | False
Widget A     | 39.99      | 2024-03-15      | NULL          | True
```

**Big-O Analysis:**
- **Time:** O(N log N) — sort by `(product_name, effective_date)` dominates; `shift()` / `LEAD()` are O(N)
- **Space:** O(N) — one output row per price event (the table can only grow over time, never shrinks with new prices)

**Evaluation Criteria:**
- `effective_end` is correctly set to the *next* event's `effective_start` for the same product — not today's date
- `is_current = True` only for the row with `effective_end IS NULL` (the open-ended, still-active period)
- Handles products with only one price event (Gizmo C): a single row with `effective_end = NULL`
- Does not confuse SCD Type 2 (new row per change) with SCD Type 1 (overwrite) or Type 3 (add a column)

**Follow-Up Probes:**
- "How would you query this SCD Type 2 table to find the price of Widget A on 2024-02-15?"
- "What's the difference between SCD Type 1, Type 2, and Type 3? When would you choose each?"
- "If you receive a price update that's *backdated* (effective_date earlier than an existing row), how would you handle it?"
- "How does a SCD Type 2 table interact with a fact table that records `unit_price` directly on each transaction? Is the SCD still needed?"

---
## MCQ Bank

**Q1 (Stage 1):** *"What are the main components of a star schema?"*
- A) One or more staging tables surrounded by raw data tables (Incorrect)
- B) A central fact table connected to multiple denormalized dimension tables via foreign keys (Correct)
- C) Multiple fact tables connected to each other in a chain (Incorrect)
- D) A single denormalized table containing everything (Incorrect)
- **Explanation:** A star schema's fact table sits at the center, containing numeric measures (revenue, quantity) and foreign keys to dimension tables. Dimension tables radiate outward, providing descriptive context (product details, date attributes, customer info). The name comes from the ER diagram resembling a star. It's the foundation of Kimball-methodology data warehouses and is optimized for OLAP queries — power BI tools like Tableau and Power BI natively understand star schema relationships. Contrast with a snowflake schema (normalized dimensions) or a single wide flat table (no normalization at all).

**Q2 (Stage 2):** *"What is the difference between additive, semi-additive, and non-additive facts?"*
- A) They describe how facts can be aggregated across dimensions (Correct)
- B) They describe how many dimension tables connect to the fact table (Incorrect)
- C) They describe the size of the fact table (Incorrect)
- D) They are different types of primary keys (Incorrect)
- **Explanation:** **Additive facts** (revenue, quantity, `total_amount`) can be summed meaningfully across ALL dimensions — total revenue by product, by customer, by date, or all combined. **Semi-additive facts** (account balance, inventory level) can be summed across some dimensions (e.g., by product) but not across time — you take a snapshot or average over periods instead of summing. **Non-additive facts** (unit_price, ratios, percentages) cannot be summed — you must aggregate the underlying components (`total_amount = unit_price × quantity`) and then compute the ratio. Misclassifying facts causes incorrect KPIs, which is why identifying the fact type is a critical step in data model design.

**Q3 (Stage 3):** *"What is the difference between OLTP and OLAP?"*
- A) OLTP is for analytics; OLAP is for transactions (Incorrect)
- B) OLTP handles transactional operations (INSERT/UPDATE); OLAP handles analytical queries (aggregations, reporting) (Correct)
- C) They are the same thing with different names (Incorrect)
- D) OLAP systems are always slower than OLTP systems (Incorrect)
- **Explanation:** **OLTP** (Online Transaction Processing): uses normalized schemas (3NF), optimized for low-latency writes (INSERT/UPDATE/DELETE), handles thousands of short transactions per second — e.g., PostgreSQL or MySQL powering a checkout page. **OLAP** (Online Analytical Processing): uses denormalized schemas (star/snowflake), optimized for complex reads aggregating millions of rows — e.g., Snowflake, BigQuery, Redshift powering BI dashboards. Data warehouses are OLAP systems fed by OLTP sources via ETL/ELT pipelines. The KPI query in Stage 3 is a pure OLAP workload — it would be painfully slow on a normalized OLTP schema without a data warehouse layer.

**Q4 (Stage 4):** *"What is the Kimball vs Inmon methodology?"*
- A) Kimball builds top-down enterprise models; Inmon builds bottom-up dimensional marts (Incorrect)
- B) Kimball builds bottom-up dimensional data marts; Inmon builds a top-down enterprise data warehouse in 3NF first (Correct)
- C) They are the same methodology (Incorrect)
- D) Kimball only works with cloud data warehouses (Incorrect)
- **Explanation:** **Kimball (bottom-up):** Build star-schema data marts per business process (a sales mart, an inventory mart), then integrate them via a data warehouse bus with conformed dimensions. Delivers business value faster, is business-friendly, and is the dominant approach in modern analytics engineering. **Inmon (top-down):** Build a single enterprise data warehouse in 3NF first (normalized, source-aligned), then derive star-schema data marts for reporting. More rigorous and avoids analytical inconsistency across departments, but slower to deliver and harder to maintain. Most modern teams use a hybrid **medallion architecture** (bronze → silver → gold layers) that shares ideas from both: Inmon-style raw/staging layers + Kimball-style star schema gold layer built with dbt.
