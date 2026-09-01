import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data_to_sqlite():
    # 1. Read cleaned CSV
    logging.info("Reading nasa_cneos_cleaned.csv...")
    df = pd.read_csv('nasa_cneos_cleaned.csv')

    # 2. Connect to local SQLite database (creates 'nasa_cneos.db' automatically)
    conn = sqlite3.connect('nasa_cneos.db')

    # 3. Load DataFrame into database table
    logging.info("Loading data into 'fact_asteroid_approaches' table...")
    df.to_sql(
        name='fact_asteroid_approaches',
        con=conn,
        if_exists='replace',
        index=False
    )
    
    conn.close()
    logging.info("Data successfully loaded into nasa_cneos.db!")

if __name__ == '__main__':
    load_data_to_sqlite()