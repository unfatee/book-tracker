import csv
from io import StringIO

from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.user import User


CSV_FIELDS = [
    "title",
    "author",
    "genre",
    "status",
    "rating",
    "total_pages",
    "current_page",
    "progress_percent",
    "start_date",
    "finish_date",
    "is_favorite",
]


def export_books_csv(db: Session, user: User) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS)
    writer.writeheader()

    books = db.query(Book).filter(Book.user_id == user.id).order_by(Book.title.asc()).all()
    for book in books:
        writer.writerow(
            {
                "title": book.title,
                "author": book.author,
                "genre": book.genre or "",
                "status": book.status,
                "rating": book.rating or "",
                "total_pages": book.total_pages,
                "current_page": book.current_page,
                "progress_percent": book.progress_percent,
                "start_date": book.start_date.isoformat() if book.start_date else "",
                "finish_date": book.finish_date.isoformat() if book.finish_date else "",
                "is_favorite": book.is_favorite,
            }
        )

    return output.getvalue()
