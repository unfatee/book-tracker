from calendar import month_name
from collections import Counter, defaultdict
from datetime import date

from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.reading_goal import ReadingGoal
from app.models.user import User
from app.schemas.analytics import (
    GenreAnalyticsItem,
    MonthlyReadingItem,
    RecentActivityItem,
    SummaryResponse,
    TopAuthorItem,
)
from app.utils.dates import today


def _user_books(db: Session, user: User) -> list[Book]:
    return db.query(Book).filter(Book.user_id == user.id).all()


def get_summary(db: Session, user: User) -> SummaryResponse:
    books = _user_books(db, user)
    current_year = today().year
    completed_this_year = [
        book for book in books
        if book.status == "completed" and book.finish_date and book.finish_date.year == current_year
    ]
    ratings = [book.rating for book in books if book.rating is not None]
    goal = (
        db.query(ReadingGoal)
        .filter(ReadingGoal.user_id == user.id, ReadingGoal.year == current_year)
        .first()
    )
    goal_progress = round((len(completed_this_year) / goal.target_books) * 100, 2) if goal else None

    return SummaryResponse(
        total_books=len(books),
        completed_books=sum(book.status == "completed" for book in books),
        reading_books=sum(book.status == "reading" for book in books),
        want_to_read_books=sum(book.status == "want_to_read" for book in books),
        paused_books=sum(book.status == "paused" for book in books),
        dropped_books=sum(book.status == "dropped" for book in books),
        favorite_books=sum(book.is_favorite for book in books),
        total_pages_read=sum(book.current_page for book in books),
        average_rating=round(sum(ratings) / len(ratings), 2) if ratings else None,
        current_year_completed=len(completed_this_year),
        current_year_goal=goal.target_books if goal else None,
        current_year_goal_progress=goal_progress,
    )


def get_by_genre(db: Session, user: User) -> list[GenreAnalyticsItem]:
    data: dict[str, dict[str, int]] = defaultdict(lambda: {"books_count": 0, "completed_count": 0, "pages_read": 0})
    for book in _user_books(db, user):
        genre = book.genre or "Uncategorized"
        data[genre]["books_count"] += 1
        data[genre]["completed_count"] += 1 if book.status == "completed" else 0
        data[genre]["pages_read"] += book.current_page
    return [GenreAnalyticsItem(genre=genre, **values) for genre, values in sorted(data.items())]


def get_monthly_reading(db: Session, user: User, year: int) -> list[MonthlyReadingItem]:
    counts = Counter(
        book.finish_date.month
        for book in _user_books(db, user)
        if book.status == "completed" and book.finish_date and book.finish_date.year == year
    )
    return [
        MonthlyReadingItem(month=month_name[index], completed_books=counts.get(index, 0))
        for index in range(1, 13)
    ]


def get_top_authors(db: Session, user: User) -> list[TopAuthorItem]:
    data: dict[str, dict[str, int]] = defaultdict(lambda: {"books_count": 0, "completed_count": 0})
    for book in _user_books(db, user):
        data[book.author]["books_count"] += 1
        data[book.author]["completed_count"] += 1 if book.status == "completed" else 0
    ordered = sorted(data.items(), key=lambda item: item[1]["books_count"], reverse=True)
    return [TopAuthorItem(author=author, **values) for author, values in ordered[:10]]


def get_recent_activity(db: Session, user: User, limit: int = 8) -> list[RecentActivityItem]:
    books = (
        db.query(Book)
        .filter(Book.user_id == user.id)
        .order_by(Book.updated_at.desc(), Book.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        RecentActivityItem(
            id=book.id,
            title=book.title,
            author=book.author,
            status=book.status,
            progress_percent=book.progress_percent,
            updated_at=book.updated_at.isoformat(),
        )
        for book in books
    ]
