# In your dags/hello_world_dag.py file

from __future__ import annotations
import pendulum
from airflow.decorators import dag, task


@task
def hello_task():
    """This task prints the NEW hello world message."""
    print("Hello World, David has MASTERED Airflow versioning!")


@task
def dummy_structural_task():
    """
    This is the structural change from the previous version.
    """
    pass


@dag(
    dag_id="hello_world",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["example", "v3-test"],  # <-- THE ONLY CHANGE IS ADDING THIS NEW TAG
)
def hello_world_dag():
    """
    ### Hello World DAG
    A simple DAG to demonstrate execution and versioning.
    """
    hello_task()
    dummy_structural_task()


hello_world_dag()
