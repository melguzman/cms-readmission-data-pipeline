from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from pathlib import Path
import sys
import subprocess
import logging
from scripts.ingest_hrrp_data import load_hrp_csv_to_sqlite

logging.basicConfig(level=logging.INFO)

# Resolve full project root based on current file's location
dag_file = Path(__file__).resolve()
project_root = dag_file.parents[1]
sys.path.append(str(project_root / "scripts"))

default_args = { 
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag_dir = Path(__file__).resolve().parent
csv_path = dag_dir / "data" / "hospital_readmissions.csv"
db_path = dag_dir / "database" / "hospital_readmissions.db"
dbt_project_path = dag_dir / "hrrp_dbt"

def run_dbt():
    try:
        result = subprocess.run(
            ["dbt", "run"],
            cwd=str(dbt_project_path),
            text=True,
            capture_output=True,
            check=True
        )
        logging.info(f"dbt run stdout:\n{result.stdout}")
        logging.info(f"dbt run stderr:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"dbt run failed with exit code {e.returncode}")
        logging.error(f"stdout:\n{e.stdout}")
        logging.error(f"stderr:\n{e.stderr}")
        raise

with DAG(
    dag_id='hrp_ingest_pipeline',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['hrrp', 'sqlite', 'etl', 'dbt']
) as dag:

    ingest_task = PythonOperator(
        task_id='ingest_hrp_csv',
        python_callable=load_hrp_csv_to_sqlite,
        op_kwargs={
            "csv_path": str(csv_path),
            "db_path": str(db_path)
        }
    )

    dbt_run_task = PythonOperator(
        task_id='run_dbt_models',
        python_callable=run_dbt
    )

    ingest_task >> dbt_run_task