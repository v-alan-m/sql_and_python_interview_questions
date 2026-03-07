import pandas as pd
import duckdb

df = pd.DataFrame({"A": [1, 2, 3]})

# Test 1: Using local variable
my_sales = df
res1 = duckdb.query("SELECT * FROM my_sales").to_df()
print("Test 1 success")

# Test 2: Using connection registration
conn = duckdb.connect()
conn.register("dynamic_sales", df)
res2 = conn.execute("SELECT * FROM dynamic_sales").df()
print("Test 2 success")
