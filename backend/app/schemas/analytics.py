from pydantic import BaseModel


class SummaryResponse(BaseModel):
    total_books: int
    completed_books: int
    reading_books: int
    want_to_read_books: int
    paused_books: int
    dropped_books: int
    favorite_books: int
    total_pages_read: int
    average_rating: float | None
    current_year_completed: int
    current_year_goal: int | None
    current_year_goal_progress: float | None


class GenreAnalyticsItem(BaseModel):
    genre: str
    books_count: int
    completed_count: int
    pages_read: int


class MonthlyReadingItem(BaseModel):
    month: str
    completed_books: int


class TopAuthorItem(BaseModel):
    author: str
    books_count: int
    completed_count: int


class RecentActivityItem(BaseModel):
    id: int
    title: str
    author: str
    status: str
    progress_percent: float
    updated_at: str
