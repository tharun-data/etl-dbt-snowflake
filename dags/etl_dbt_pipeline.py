from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

ETL_DIR = "/mnt/c/Users/Hp/Desktop/etl_project"
DBT_DIR = "/mnt/c/Users/Hp/Desktop/etl_dbt"
PY = "/home/tharun/airflow-env/bin/python"
DBT = "/home/tharun/dbt-env/bin/dbt"

default_args = {
    "owner": "tharun",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="etl_dbt_pipeline",
    description="Python ETL (inbox -> RAW) then dbt run and test",
    default_args=default_args,
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    tags=["etl", "dbt", "snowflake"],
) as dag:

    run_etl = BashOperator(
        task_id="run_etl",
        bash_command=f"cd {ETL_DIR} && {PY} etl_pipeline.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_DIR} && {DBT} run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_DIR} && {DBT} test",
    )

    run_etl >> dbt_run >> dbt_test
