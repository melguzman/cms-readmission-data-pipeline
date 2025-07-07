<h1>🚑 Healthcare Readmission Reduction Pipeline</h1>
A data pipeline to ingest, transform, and visualize CMS Hospital Readmissions Reduction Program (HRRP) data.

This project automates:

- Loading HRRP CSV data into SQLite
- Data cleaning & transformations using dbt
- Analytics & dashboards in Tableau

<h2>🗃️ Data Source</h2>

- [CMS Hospital Readmissions Reduction Program](https://data.cms.gov/provider-data/dataset/9n3s-kdb3#overview)

<h2>🌐 Project Structure</h2>

```
healthcare_readmission_pipeline/
│
├── dags/
│   ├── hrp_pipeline_dag.py
│   └── scripts/
│       └── ingest_hrrp_data.py
│
├── hrrp_dbt/
│   ├── dbt_project.yml
│   ├── models/
│   ├── macros/
│   └── target/          # Ignored in git
│
├── tableau/
│   ├── dashboard.twb
│   ├── top_bottom_hospitals.csv
│   ├── penalty_trends.csv
│   └── stg_hospital_readmissions.csv
│
├── requirements.txt
└── README.md
```

<h2>⚙️ How It Works</h2>
1. Data Ingestion
- Source file: hospital_readmissions.csv
- Loaded into SQLite DB table: raw_hospital_readmissions
- Done via Airflow Python task:

```bash
scripts/ingest_hrrp_data.py
```

2. Data Transformation (dbt)
- dbt transforms raw data into clean, analysis-ready tables:
- stg_hospital_readmissions
- hospital_penalties
- penalty_trends
- top_bottom_hospitals

Key transformations include:
- Type casting numeric fields
- Parsing dates into proper formats
- Calculating fiscal years
- Deriving penalty metrics

Run locally:

```bash
cd hrrp_dbt
dbt run
```

3. Dashboard (Tableau)
- Connect Tableau to:
- CSV exports of dbt models
- Visualizations include:
- National map of penalties by state
- Trends in penalties over time
- Filters by medical condition
- Top/bottom 10 hospitals

Note: For Tableau Public, CSV extracts are used instead of live DB connections.

<h2>🚀 Running the Pipeline</h2>

Prerequisites
- Python 3.10
- Airflow
- dbt-core
- SQLite
- Tableau Desktop (Public Edition)

Install dependencies:
```bash
pip install -r requirements.txt
```

Run Airflow
Start Airflow:
```bash
airflow standalone
```
Trigger the DAG manually in Airflow UI:
- DAG ID: hrp_ingest_pipeline

Or via CLI:
```bash
airflow dags trigger hrp_ingest_pipeline
```
This will:

- Load CSV into SQLite
- Run dbt transformations
- Generate output CSVs for Tableau

Open Tableau Dashboard
1. Launch Tableau Desktop
2. Open:
```bash
tableau/dashboard.twb
```
3. Explore:
- Maps
- Time trends
- Filters for Top/Bottom hospitals

Completed Visuals
- National map of penalties by state
- Condition filters (heart failure, pneumonia, etc.)
- Top/bottom 10 hospitals by penalties

<h2>✨ Future Improvements</h2>

- Deploy Airflow & dbt in cloud
- Integrate additional CMS datasets

<h2>Quick Start</h2>

```bash
# Run pipeline end-to-end:
airflow dags trigger hrp_ingest_pipeline

# OR run dbt manually:
cd hrrp_dbt
dbt run
```