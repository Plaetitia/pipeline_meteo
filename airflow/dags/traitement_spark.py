from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "laetitia",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    "traitement_spark",
    default_args=default_args,
    schedule_interval="@hourly",
    catchup=False,
) as dag:

    task_spark_transform = BashOperator(
        task_id="run_spark_job",
        bash_command="python /opt/airflow/src/spark/spark_job.py",
    )