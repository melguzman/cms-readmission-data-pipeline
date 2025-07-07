import pandas as pd
import sqlite3
import logging
from pathlib import Path

def load_hrp_csv_to_sqlite(
    csv_path,
    db_path,
    table_name='raw_hospital_readmissions'
):
    try:
        csv_path = Path(csv_path)
        db_path = Path(db_path)

        logging.info(f"Starting to load data from {csv_path} into {db_path} (table: {table_name})")

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        df = pd.read_csv(csv_path)
        logging.info(f"CSV loaded successfully with {len(df)} rows.")

        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        db_dir = db_path.parent
        db_dir.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()

        logging.info(f"Loaded {len(df)} records into {table_name} table successfully.")

    except Exception as e:
        logging.error(f"Error loading CSV to SQLite: {e}")
        raise
