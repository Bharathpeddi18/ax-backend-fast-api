# AX Backend API

FastAPI backend for Astrax School, a student management platform that improves communication between parents and schools.

## Features

- REST APIs to create, retrieve, update, and delete student profiles
- Password hashing with Argon2 and JWT-based authentication
- Role-based authorization
- PostgreSQL with SQLAlchemy and Alembic database migrations
- Service-based architecture
- CI/CD: every merged pull request to `master` deploys automatically to Microsoft Azure

## Tech Stack

Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic, PyJWT, Argon2

## Getting Started

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Create a `.env` file with your database and application settings before starting the server.

API docs are available at http://localhost:8000/docs once the server is running.

## Frontend

The Next.js frontend is in [ax-reusable-components](https://github.com/Bharathpeddi18/ax-reusable-components).

## Author

Bharath Kumar Peddi - [LinkedIn](https://www.linkedin.com/in/bharath-kumar-peddi-881a90253/)
