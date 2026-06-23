from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import analytics, auth, books, export, goals, quotes


app = FastAPI(
    title="Book Tracker API",
    description="API for tracking books, reading progress, quotes and analytics.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(export.router)
app.include_router(books.router)
app.include_router(quotes.router)
app.include_router(goals.router)
app.include_router(analytics.router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "book-tracker-api"}
