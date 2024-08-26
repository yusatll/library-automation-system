# Library Automation System

This project implements a library automation system using FastAPI, Celery, and Docker.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Build and run the Docker containers:
   ```
   docker build -t fastapp . 

   docker run -p 8000:8000 fastapp
   ```

2. Access the FastAPI application at `http://localhost:8000`


## Project Structure

- `app/`: Contains the FastAPI application
- `celery_app/`: Contains Celery tasks and configuration
- `tests/`: Contains test files
- `Dockerfile`: Defines the Docker image for the application
- `docker-compose.yml`: Defines the services for the application stack
- `requirements.txt`: Lists the Python dependencies

## Celery Tasks

Celery tasks are scheduled using Celery Beat. The current schedule is:

- Send overdue reminders: Daily at 9:00 AM
- Generate weekly report: Weekly on Sunday at midnight
