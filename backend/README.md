# Book Tracker Backend

FastAPI backend for Book Tracker. It provides JWT authentication, protected CRUD endpoints for books and quotes, reading goals, analytics, demo data and CSV export.

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

By default the app reads `.env` from this directory or inherited environment variables. For Docker, `docker-compose.yml` provides the PostgreSQL connection string.

## Tests

```bash
pytest
```

The tests override the database dependency with SQLite, so they run without PostgreSQL.
