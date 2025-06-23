#
# This is the corrected, modern version of your DAG
#
from __future__ import annotations

import pendulum

from airflow.decorators import dag, task


@task
def hello_world():
    """This is the task implementation."""
    print("Hello World, David is gonna be super successful. Really. ")


@dag(
    dag_id="hello_world",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    description="A simple Hello World DAG",
    schedule=None,
    catchup=False,
    tags=["example"],
    version="1.1.0",  # <-- The version parameter now works correctly here
)
def hello_world_dag():
    """
    ### Hello World DAG
    This DAG prints a hello world message.
    """
    # This calls your task function to create an instance of the task
    hello_world()


# This final line instantiates the DAG
hello_world_dag()
