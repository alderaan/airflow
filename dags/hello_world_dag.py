# In your dags/hello_world_dag.py file

from __future__ import annotations

import pendulum

from airflow.decorators import dag, task


@task
def hello_task():
    """This task prints the first hello world message."""
    print("Hello World, David is gonna be self employed!")


@dag(
    dag_id="hello_world",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["example"],
)
def hello_world_dag():
    """
    ### Hello World DAG
    A simple DAG to demonstrate execution and versioning.
    This is the first version of the DAG.
    """
    # This calls your task function to create an instance of the task in the DAG
    hello_task()


# This final line instantiates the DAG and makes it available to Airflow
hello_world_dag()
