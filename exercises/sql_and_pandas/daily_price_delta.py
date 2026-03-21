import pandas as pd

def get_exercise():
    return {
        "title": "Daily Price Delta",
        "subtitle": "Window Functions, Pandas Aggregation",
        "description": "Calculate the difference in closing price between the current day and the previous day for a given stock.",
        "data": pd.DataFrame({
            "date": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"],
            "ticker": ["AAPL", "AAPL", "AAPL", "AAPL"],
            "close_price": [150.0, 155.0, 153.0, 158.0]
        }),
        "table_name": "stock_prices",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "Ensure the data is sorted by date. Then use the `.shift()` method on the 'close_price' column to get the previous day's price and subtract it from the current day's price.",
        "hint_sql": "Use the `LAG()` window function to retrieve the close price from the previous row, ordered by date. Then calculate the difference.",
        "solution_python": """
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by=["ticker", "date"]).reset_index(drop=True)

df["price_delta"] = df["close_price"] - df.groupby("ticker")["close_price"].shift(1)
result = df
""",
        "solution_sql": """
SELECT 
    date,
    ticker,
    close_price,
    close_price - LAG(close_price, 1) OVER (PARTITION BY ticker ORDER BY date ASC) AS price_delta
FROM stock_prices
ORDER BY ticker, date ASC;
""",
        "deep_dive": "The `LAG()` function in SQL and `.shift()` method in Pandas allow for accessing data from previous rows without needing complex joins. Both operations run in O(N) time after the required O(N log N) sorting step.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Single Stock, Pre-Sorted",
                "scenario": "Let's start simple. You have a dataset of a single stock (AAPL) where the rows are already ordered by date. Can you calculate the `price_delta` — the difference between the current day's closing price and the previous day's closing price?",
                "hint": "Python: Use the `.shift(1)` method on the 'close_price' column to get the previous row's value. SQL: Use the `LAG()` window function over an `ORDER BY` clause to peak at the previous row.",
                "data": pd.DataFrame({
                    "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
                    "ticker": ["AAPL", "AAPL", "AAPL"],
                    "close_price": [150.0, 155.0, 153.0]
                }),
                "evaluation_criteria": [
                    "Window functions/row traversal in SQL (`LAG`).",
                    "Basic row shifting in Python (`.shift()`).",
                    "Handling of the first day (which will naturally evaluate to `NaN`/`NULL` since there is no previous day)."
                ],
                "solution_code": """\
df["date"] = pd.to_datetime(df["date"])
df["price_delta"] = df["close_price"] - df["close_price"].shift(1)
result = df
""",
                "solution_sql": """\
SELECT 
    date,
    ticker,
    close_price,
    close_price - LAG(close_price, 1) OVER (ORDER BY date ASC) AS price_delta
FROM stock_prices
ORDER BY date ASC;
""",
                "expected_output": pd.DataFrame({
                    "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
                    "ticker": ["AAPL", "AAPL", "AAPL"],
                    "close_price": [150.0, 155.0, 153.0],
                    "price_delta": [float('nan'), 5.0, -2.0]
                }),
                "follow_up_probes": [
                    "What is the value of `price_delta` on the very first day?",
                    "What would happen if the dates were not consecutive?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Multiple Stocks",
                "scenario": "Now we're tracking multiple stocks in the same table, though the rows are still pre-sorted by ticker and date. How do you ensure you only calculate the price difference within the same stock, so Apple's price isn't compared to Microsoft's?",
                "hint": "Python: Combine `.groupby(\"ticker\")` with `.shift(1)`. SQL: Add a `PARTITION BY` clause to your window function.",
                "data": pd.DataFrame({
                    "date": ["2023-01-01", "2023-01-02", "2023-01-01", "2023-01-02"],
                    "ticker": ["AAPL", "AAPL", "MSFT", "MSFT"],
                    "close_price": [150.0, 155.0, 250.0, 255.0]
                }),
                "evaluation_criteria": [
                    "Understanding grouped operations / partitioning.",
                    "Ensuring values do not 'bleed over' between groups when shifting rows."
                ],
                "solution_code": """\
df["date"] = pd.to_datetime(df["date"])
df["price_delta"] = df["close_price"] - df.groupby("ticker")["close_price"].shift(1)
result = df
""",
                "solution_sql": """\
SELECT 
    date,
    ticker,
    close_price,
    close_price - LAG(close_price, 1) OVER (PARTITION BY ticker ORDER BY date ASC) AS price_delta
FROM stock_prices
ORDER BY ticker, date ASC;
""",
                "expected_output": pd.DataFrame({
                    "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-01", "2023-01-02"]),
                    "ticker": ["AAPL", "AAPL", "MSFT", "MSFT"],
                    "close_price": [150.0, 155.0, 250.0, 255.0],
                    "price_delta": [float('nan'), 5.0, float('nan'), 5.0]
                }),
                "follow_up_probes": [
                    "How does `groupby` combined with `.shift()` behave internally in Pandas?",
                    "Without `PARTITION BY` in SQL, what erroneous calculation would appear on row 3?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Unsorted Data",
                "scenario": "Real-world data is rarely pristine. Your incoming data source has changed and now rows can arrive in any order. Modify your code to calculate the correct daily delta regardless of the input order, returning the results ordered by ticker then date.",
                "hint": "Python: Sort the dataframe by ticker and date before performing the shift calculation. SQL: The window function's `ORDER BY` handles the sequence *for the calculation*, but you must also ensure the final output is sorted.",
                "data": pd.DataFrame({
                    "date": ["2023-01-02", "2023-01-01", "2023-01-03", "2023-01-01", "2023-01-02"],
                    "ticker": ["AAPL", "AAPL", "AAPL", "MSFT", "MSFT"],
                    "close_price": [155.0, 150.0, 153.0, 250.0, 255.0]
                }),
                "evaluation_criteria": [
                    "Identifying implicit assumptions (data sorting).",
                    "State management and reassigning variables cleanly in Python.",
                    "Understanding the difference between `ORDER BY` inside an `OVER` clause vs the main query `ORDER BY` in SQL."
                ],
                "solution_code": """\
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by=["ticker", "date"]).reset_index(drop=True)
df["price_delta"] = df["close_price"] - df.groupby("ticker")["close_price"].shift(1)
result = df
""",
                "solution_sql": """\
SELECT 
    date,
    ticker,
    close_price,
    close_price - LAG(close_price, 1) OVER (PARTITION BY ticker ORDER BY date ASC) AS price_delta
FROM stock_prices
ORDER BY ticker, date ASC;
""",
                "expected_output": pd.DataFrame({
                    "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-01", "2023-01-02"]),
                    "ticker": ["AAPL", "AAPL", "AAPL", "MSFT", "MSFT"],
                    "close_price": [150.0, 155.0, 153.0, 250.0, 255.0],
                    "price_delta": [float('nan'), 5.0, -2.0, float('nan'), 5.0]
                }),
                "follow_up_probes": [
                    "What is the time complexity of your sorting step?",
                    "If we had millions of stocks, how would sorting impact memory and performance?"
                ]
            }
        ]
    }
