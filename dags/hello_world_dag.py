# In your dags/hello_world_dag.py file (replace the old content)

from __future__ import annotations

import pendulum

from airflow.decorators import dag, task


@task
def hello_task():
    """This task prints the NEW hello world message."""
    # 1. This is your implementation change
    print("Hello World, David has MASTERED Airflow versioning!")


@task
def dummy_structural_task():
    """
    2. This is a structural change. The existence of this new task
       will create a new DAG Version in the UI.
    """
    pass


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
    This is the second version of the DAG, with a structural change.
    """
    # Call both tasks to include them in the DAG
    hello_task()
    dummy_structural_task()


# This final line instantiates the DAG
hello_world_dag()
