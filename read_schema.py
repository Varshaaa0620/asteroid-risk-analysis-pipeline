import sqlite3
import pandas as pd

conn = sqlite3.connect('nasa_cneos.db')

# 1. Print all column names and data types
print("--- DATABASE SCHEMA (Columns & Types) ---")
schema_info = pd.read_sql_query("PRAGMA table_info(fact_asteroid_approaches);", conn)
print(schema_info[['cid', 'name', 'type']])

# 2. Print the first 3 rows of actual data
print("\n--- SAMPLE ROWS ---")
sample_data = pd.read_sql_query("SELECT * FROM fact_asteroid_approaches LIMIT 3;", conn)
print(sample_data)

conn.close()