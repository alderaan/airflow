#!/bin/bash

# Deploy script for Airflow DAGs - triggered by n8n webhook
# This script pulls latest changes (DAGs are auto-detected by Airflow)

set -e  # Exit on any error

# Configuration
AIRFLOW_DIR="/home/david/airflow"
GIT_BRANCH="main"  # Change this to your default branch

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Pulling latest DAG changes..."

# Change to Airflow directory
cd "$AIRFLOW_DIR" || {
    echo "ERROR: Could not change to directory $AIRFLOW_DIR"
    exit 1
}

# Pull latest changes
git fetch origin
git reset --hard origin/$GIT_BRANCH

echo "[$(date '+%Y-%m-%d %H:%M:%S')] DAG changes pulled successfully"
echo "Airflow will automatically detect new DAGs within 30 seconds" 