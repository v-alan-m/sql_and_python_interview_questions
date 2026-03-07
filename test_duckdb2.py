import pandas as pd
import duckdb

def test_fn():
    df = pd.DataFrame({"A": [1, 2, 3]})
    table_name = "daily_revenue"
    
    # Can we just register globally?
    duckdb.register(table_name, df)
    res = duckdb.query("SELECT * FROM daily_revenue").to_df()
    print("Test success:", res.shape)

test_fn()
