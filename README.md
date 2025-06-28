# Dockerized Airflow 3

A production-ready Apache Airflow 3 deployment running on a VPS with Docker Compose.

## Overview

This repository contains a complete Airflow 3 setup using Docker Compose with:
- **CeleryExecutor** for distributed task execution
- **PostgreSQL** as the metadata database
- **Redis** as the message broker
- **GitDAGBundle** for automatic DAG synchronization
- **Custom Dockerfile** for additional dependencies

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Server    │    │   Scheduler     │    │   DAG Processor │
│   (Port 8081)   │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Celery Workers │
                    │   (Scalable)    │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Redis       │    │   Triggerer     │
│   (Database)    │    │  (Message Bus)  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Features

- **Automatic DAG Sync**: GitDAGBundle pulls latest DAGs every 60 seconds
- **Custom Dependencies**: Dockerfile installs Git client and Airflow Git provider
- **Production Ready**: Configured for VPS deployment with proper health checks
- **Scalable**: Celery workers can be scaled horizontally
- **Secure**: Environment-based configuration with secrets management

## Configuration

### Environment Variables

Environment variables that are explicitly set in `docker-compose.yaml` are commented out in `airflow.cfg` to avoid confusion. This ensures a single source of truth for configuration.

### Required .env File

Create a `.env` file in the root directory with the following variables:

```bash
# Airflow Core Configuration
AIRFLOW__CORE__FERNET_KEY=your_fernet_key_here

# Git Repository Connection
AIRFLOW_CONN_MY_GIT_REPO=git+https://username:password@github.com/your-repo.git

# DAG Bundle Configuration
AIRFLOW__DAG_PROCESSOR__DAG_BUNDLE_CONFIG_LIST=[{"repo_url": "git+https://username:password@github.com/your-repo.git", "branch": "main", "subfolder": "dags"}]

# Additional Requirements (optional)
_PIP_ADDITIONAL_REQUIREMENTS=package1==1.0.0 package2==2.0.0
```

**⚠️ Security Note**: Never commit your `.env` file to version control. Add it to `.gitignore`.

## Deployment

### Prerequisites

- Docker and Docker Compose installed on your VPS
- Git repository with your DAGs
- Proper network access and firewall configuration

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd airflow
   ```

2. **Create the .env file**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Set proper permissions**:
   ```bash
   export AIRFLOW_UID=50000
   ```

4. **Start the services**:
   ```bash
   docker compose up -d
   ```

5. **Initialize the database** (first time only):
   ```bash
   docker compose up airflow-init
   ```

6. **Access the web UI**:
   - URL: `http://your-vps-ip:8081`
   - Default credentials: `airflow` / `airflow`

### Environment Variables in Docker Compose

The following key configurations are set in `docker-compose.yaml`:

- **Executor**: `CeleryExecutor` for distributed processing
- **Database**: PostgreSQL connection string
- **Message Broker**: Redis URL
- **Web Server**: Proxy settings for production deployment
- **DAG Bundle**: Git repository configuration for automatic DAG sync

## DAG Management

### Automatic Sync

The GitDAGBundle automatically:
- Pulls DAGs from your Git repository every 60 seconds
- Supports multiple repositories and branches
- Handles authentication via Git credentials
- Updates DAGs without service restart

### Manual DAG Operations

```bash
# List all DAGs
docker compose exec airflow-scheduler airflow dags list

# Test a specific DAG
docker compose exec airflow-scheduler airflow dags test <dag_id>

# Trigger a DAG run
docker compose exec airflow-scheduler airflow dags trigger <dag_id>
```

## Monitoring

### Service Status
```bash
docker compose ps
```

### Logs
```bash
# All services
docker compose logs

# Specific service
docker compose logs airflow-scheduler
docker compose logs airflow-worker
```

### Health Checks
All services include health checks:
- Database connectivity
- Message broker availability
- Airflow service health

## Scaling

### Scale Workers
```bash
# Scale to 3 workers
docker compose up -d --scale airflow-worker=3
```

### Resource Limits
Adjust resource limits in `docker-compose.yaml` for your VPS specifications.

## Maintenance

### Database Backup
```bash
docker compose exec postgres pg_dump -U airflow airflow > backup.sql
```

### Update Airflow
1. Update the image tag in `docker-compose.yaml`
2. Rebuild the custom image: `docker compose build`
3. Restart services: `docker compose up -d`

### Rotate Fernet Key
1. Generate new key: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
2. Update `.env` file
3. Restart services

## Troubleshooting

### Common Issues

1. **Permission Errors**
   - Ensure `AIRFLOW_UID` is set correctly
   - Check file permissions on mounted volumes

2. **DAG Sync Issues**
   - Verify Git repository credentials
   - Check network connectivity
   - Review DAG bundle configuration

3. **Database Connection**
   - Ensure PostgreSQL is healthy
   - Check connection string format

### Useful Commands

```bash
# Check Airflow version
docker compose exec airflow-scheduler airflow version

# Reset database (⚠️ destructive)
docker compose down -v
docker compose up airflow-init

# View scheduler health
docker compose exec airflow-scheduler airflow jobs check
```

## Security Best Practices

- Use strong, unique passwords
- Keep `.env` file secure
- Regularly rotate Fernet key
- Use HTTPS in production
- Consider secrets management
- Limit network access to Airflow services

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Airflow documentation
3. Check service logs
4. Verify configuration values

## License

Apache License 2.0 