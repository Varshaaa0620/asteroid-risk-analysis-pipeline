import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('nasa_cneos.db')

# QUERY 1: Top 10 Highest Risk Asteroid Threats
query_1 = """
SELECT 
    object_designation,
    close_approach_date,
    est_diameter_m,
    miss_distance_ld,
    velocity_km_s,
    risk_score,
    risk_level
FROM fact_asteroid_approaches
WHERE risk_level = 'High Priority'
ORDER BY risk_score DESC
LIMIT 10;
"""

print("\n=======================================================")
print("          QUERY 1: TOP 10 HIGH PRIORITY THREATS        ")
print("=======================================================")
df_results1 = pd.read_sql_query(query_1, conn)
print(df_results1.to_string(index=False))


# QUERY 2: Risk Level Breakdown & Aggregate Metrics
query_2 = """
SELECT 
    risk_level,
    COUNT(*) AS total_asteroids,
    ROUND(AVG(miss_distance_ld), 2) AS avg_miss_distance_ld,
    ROUND(AVG(velocity_km_s), 2) AS avg_velocity_kms,
    ROUND(MAX(est_diameter_m), 1) AS max_diameter_m
FROM fact_asteroid_approaches
GROUP BY risk_level;
"""

print("\n=======================================================")
print("          QUERY 2: RISK TIER SUMMARY MATRIX            ")
print("=======================================================")
df_results2 = pd.read_sql_query(query_2, conn)
print(df_results2.to_string(index=False))

# Close the database connection
conn.close()