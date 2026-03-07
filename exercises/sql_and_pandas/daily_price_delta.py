import pandas as pd

def get_exercise():
    return {
        "title": "Daily Price Delta",
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
        "deep_dive": "The `LAG()` function in SQL and `.shift()` method in Pandas allow for accessing data from previous rows without needing complex joins. Both operations run in O(N) time after the required O(N log N) sorting step."
    }
