# Start from the official Airflow image
FROM apache/airflow:3.0.2

# Switch to the root user to install system packages
USER root

# Install the git client using the system package manager
RUN apt-get update && apt-get install -y --no-install-recommends git

# Switch back to the non-privileged airflow user
USER airflow

# Install the required Airflow provider package
RUN pip install --no-cache-dir "apache-airflow-providers-git"