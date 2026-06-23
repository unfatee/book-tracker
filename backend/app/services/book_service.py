from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.quote import Quote
from app.models.reading_goal import ReadingGoal
from app.models.user import User
from app.schemas.book import BookCreate, BookProgressUpdate, BookStatusUpdate, BookUpdate
from app.utils.dates import today


VALID_STATUSES = {"want_to_read", "reading", "completed", "paused", "dropped"}
SORT_COLUMNS = {
    "title": Book.title,
    "author": Book.author,
    "created_at": Book.created_at,
    "updated_at": Book.updated_at,
    "rating": Book.rating,
    "finish_date": Book.finish_date,
}


def get_book_or_404(db: Session, user: User, book_id: int) -> Book:
    book = db.query(Book).filter(Book.id == book_id, Book.user_id == user.id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


def _validate_pages(total_pages: int, current_page: int) -> None:
    if total_pages <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="total_pages must be greater than 0")
    if current_page < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="current_page cannot be negative")
    if current_page > total_pages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="current_page cannot be greater than total_pages",
        )


def _apply_book_rules(fields: dict, existing: Book | None = None) -> dict:
    total_pages = fields.get("total_pages", existing.total_pages if existing else None)
    current_page = fields.get("current_page", existing.current_page if existing else 0)
    status_value = fields.get("status", existing.status if existing else "want_to_read")
    start_date = fields.get("start_date", existing.start_date if existing else None)
    finish_date = fields.get("finish_date", existing.finish_date if existing else None)

    if status_value not in VALID_STATUSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book status")

    _validate_pages(total_pages, current_page)

    if status_value == "completed":
        fields["current_page"] = total_pages
        fields["finish_date"] = finish_date or today()
    elif current_page == total_pages:
        fields["status"] = "completed"
        fields["finish_date"] = finish_date or today()
    elif status_value == "reading" and not start_date:
        fields["start_date"] = today()

    return fields


def list_books(
    db: Session,
    user: User,
    status_filter: str | None = None,
    genre: str | None = None,
    rating: int | None = None,
    is_favorite: bool | None = None,
    search: str | None = None,
    sort_by: str = "updated_at",
    sort_order: str = "desc",
) -> list[Book]:
    query = db.query(Book).filter(Book.user_id == user.id)

    if status_filter:
        query = query.filter(Book.status == status_filter)
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    if rating is not None:
        query = query.filter(Book.rating == rating)
    if is_favorite is not None:
        query = query.filter(Book.is_favorite == is_favorite)
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(Book.title.ilike(pattern), Book.author.ilike(pattern)))

    books = query.all()
    reverse = sort_order.lower() != "asc"
    if sort_by == "progress":
        return sorted(books, key=lambda book: book.progress_percent, reverse=reverse)

    sort_column = SORT_COLUMNS.get(sort_by, Book.updated_at)
    ordered = query.order_by(sort_column.desc() if reverse else sort_column.asc()).all()
    return ordered


def create_book(db: Session, user: User, payload: BookCreate) -> Book:
    fields = _apply_book_rules(payload.model_dump())
    book = Book(user_id=user.id, **fields)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, user: User, book_id: int, payload: BookUpdate) -> Book:
    book = get_book_or_404(db, user, book_id)
    fields = payload.model_dump(exclude_unset=True)
    if not fields:
        return book

    fields = _apply_book_rules(fields, existing=book)
    for key, value in fields.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, user: User, book_id: int) -> None:
    book = get_book_or_404(db, user, book_id)
    db.delete(book)
    db.commit()


def update_progress(db: Session, user: User, book_id: int, payload: BookProgressUpdate) -> Book:
    book = get_book_or_404(db, user, book_id)
    _validate_pages(book.total_pages, payload.current_page)

    book.current_page = payload.current_page
    if book.current_page == book.total_pages:
        book.status = "completed"
        book.finish_date = book.finish_date or today()
    else:
        if book.status == "completed":
            book.status = "reading" if book.current_page > 0 else "want_to_read"
            book.finish_date = None
        if book.current_page > 0 and book.status == "want_to_read":
            book.status = "reading"
            book.start_date = book.start_date or today()

    db.commit()
    db.refresh(book)
    return book


def toggle_favorite(db: Session, user: User, book_id: int) -> Book:
    book = get_book_or_404(db, user, book_id)
    book.is_favorite = not book.is_favorite
    db.commit()
    db.refresh(book)
    return book


def update_status(db: Session, user: User, book_id: int, payload: BookStatusUpdate) -> Book:
    book = get_book_or_404(db, user, book_id)
    new_status = payload.status

    if new_status == "completed":
        book.status = "completed"
        book.current_page = book.total_pages
        book.finish_date = book.finish_date or today()
    else:
        book.status = new_status
        if new_status == "want_to_read":
            book.current_page = 0
        elif new_status == "reading":
            book.start_date = book.start_date or today()
        if book.current_page == book.total_pages:
            book.current_page = max(book.total_pages - 1, 0)
        book.finish_date = None

    db.commit()
    db.refresh(book)
    return book


def create_demo_data(db: Session, user: User) -> list[Book]:
    current_year = today().year
    demo_books = [
        ("Atomic Habits", "James Clear", "Self-Development", "completed", 320, 320, 5, 1, 14),
        ("Clean Code", "Robert C. Martin", "Programming", "reading", 464, 180, 5, None, None),
        ("The Pragmatic Programmer", "Andrew Hunt, David Thomas", "Programming", "want_to_read", 352, 0, None, None, None),
        ("Dune", "Frank Herbert", "Science Fiction", "completed", 688, 688, 5, 2, 20),
        ("1984", "George Orwell", "Dystopian", "completed", 328, 328, 4, 3, 8),
        ("Deep Work", "Cal Newport", "Productivity", "paused", 304, 120, None, None, None),
        ("Project Hail Mary", "Andy Weir", "Science Fiction", "reading", 496, 250, None, None, None),
        ("The Hobbit", "J.R.R. Tolkien", "Fantasy", "want_to_read", 310, 0, None, None, None),
        ("Thinking, Fast and Slow", "Daniel Kahneman", "Psychology", "dropped", 499, 90, None, None, None),
        ("Refactoring", "Martin Fowler", "Programming", "want_to_read", 448, 0, None, None, None),
    ]

    created: list[Book] = []
    existing_titles = {
        title for (title,) in db.query(Book.title).filter(Book.user_id == user.id).all()
    }
    for title, author, genre, status_value, total_pages, current_page, rating, month, day in demo_books:
        if title in existing_titles:
            continue
        finish_date = date(current_year, month, day) if month and day else None
        start_date = date(current_year, max(month or 4, 1), 1) if status_value in {"reading", "completed", "paused", "dropped"} else None
        book = Book(
            user_id=user.id,
            title=title,
            author=author,
            genre=genre,
            status=status_value,
            total_pages=total_pages,
            current_page=current_page,
            rating=rating,
            finish_date=finish_date,
            start_date=start_date,
            description=f"A demo entry for {title} by {author}.",
            personal_notes="Added as demo data to showcase tracking, analytics and quotes.",
        )
        db.add(book)
        created.append(book)

    db.flush()

    quotes_by_title = {
        "Clean Code": [
            ("Clean code always looks like it was written by someone who cares.", 10, "A concise standard for everyday work."),
            ("The only way to go fast is to go well.", 31, "Useful when discussing technical debt."),
        ],
        "Dune": [
            ("Fear is the mind-killer.", 19, "Classic quote for the highlights list."),
        ],
        "Atomic Habits": [
            ("You do not rise to the level of your goals. You fall to the level of your systems.", 27, "Great reminder for reading habits."),
        ],
    }

    for book in created:
        for text, page, note in quotes_by_title.get(book.title, []):
            db.add(Quote(user_id=user.id, book_id=book.id, text=text, page=page, note=note))

    goal = db.query(ReadingGoal).filter(ReadingGoal.user_id == user.id, ReadingGoal.year == current_year).first()
    if goal:
        goal.target_books = max(goal.target_books, 12)
    else:
        db.add(ReadingGoal(user_id=user.id, year=current_year, target_books=12))

    db.commit()
    for book in created:
        db.refresh(book)
    return created
