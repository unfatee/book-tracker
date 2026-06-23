# Book Tracker

Book Tracker is a fullstack web application for managing a personal reading library, tracking book progress, saving quotes and notes, and analyzing reading habits.

## Problem

Readers often keep books, highlights, progress and goals in separate places. Book Tracker brings them into one private workspace with searchable books, reading status, yearly goals and useful analytics.

## Features

- User registration and JWT login
- Create, edit and delete books
- Track reading status and progress
- Save personal notes and quotes
- Mark favorite books
- Search, filter and sort books
- Reading goal tracking
- Reading analytics by genre and month
- Top authors statistics
- CSV export
- Demo data generation
- Responsive React dashboard
- PostgreSQL database
- Docker support
- Backend tests

## Tech Stack

- Backend: Python, FastAPI, SQLAlchemy, Alembic, Pydantic, JWT, passlib, PostgreSQL, Pytest
- Frontend: React, Vite, JavaScript, React Router, Axios, Context API, Recharts, CSS
- DevOps: Docker, Docker Compose

## Screenshots

Add screenshots after running the project locally:

- Dashboard with summary cards and charts
- Books page with filters
- Book detail page with progress and quotes

## Project Structure

```text
book-tracker/
  backend/
    app/
      models/
      schemas/
      routers/
      services/
      utils/
    alembic/
    tests/
  frontend/
    src/
      api/
      components/
      context/
      pages/
      utils/
  docker-compose.yml
  .env.example
  README.md
```

## Run with Docker

```bash
cd book-tracker
docker compose up --build
```

After startup:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs

## Run without Docker

Start PostgreSQL locally and create a `book_tracker` database. Then copy the example env file and adjust values if needed:

```bash
cd book-tracker
copy .env.example backend\.env
```

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/book_tracker
JWT_SECRET_KEY=change-this-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
VITE_API_BASE_URL=http://localhost:8000
```

## API Endpoints

Auth:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

Books:

- `GET /books`
- `POST /books`
- `GET /books/{book_id}`
- `PUT /books/{book_id}`
- `DELETE /books/{book_id}`
- `PATCH /books/{book_id}/progress`
- `PATCH /books/{book_id}/favorite`
- `PATCH /books/{book_id}/status`
- `POST /books/demo-data`
- `GET /books/export/csv`

Quotes:

- `GET /books/{book_id}/quotes`
- `POST /books/{book_id}/quotes`
- `PUT /books/{book_id}/quotes/{quote_id}`
- `DELETE /books/{book_id}/quotes/{quote_id}`
- `GET /quotes`

Goals:

- `GET /goals`
- `GET /goals/{year}`
- `POST /goals`
- `PUT /goals/{year}`
- `DELETE /goals/{year}`
- `GET /goals/{year}/progress`

Analytics:

- `GET /analytics/summary`
- `GET /analytics/by-genre`
- `GET /analytics/monthly-reading?year=2026`
- `GET /analytics/top-authors`
- `GET /analytics/recent-activity`

## Tests

```bash
cd backend
pytest
```

The backend test suite covers auth, book CRUD, progress updates, favorites, status updates, quote permissions, goals and analytics. Tests use SQLite through FastAPI dependency overrides, while the production Docker setup uses PostgreSQL.
