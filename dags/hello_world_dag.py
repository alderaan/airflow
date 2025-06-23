from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def hello_world():
    print(
        "Hello World, David is gonna be rich. I mean super rich. I mean, like, really rich."
    )


default_args = {
    "start_date": datetime(2024, 1, 1),
}

dag = DAG(
    "hello_world",
    default_args=default_args,
    description="A simple Hello World DAG",
    schedule=None,  # Only run manually
    catchup=False,
    tags=["example"],
)

hello_task = PythonOperator(
    task_id="hello_task",
    python_callable=hello_world,
    dag=dag,
)
