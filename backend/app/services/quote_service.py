from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.book import Book
from app.models.quote import Quote
from app.models.user import User
from app.schemas.quote import QuoteCreate, QuoteUpdate
from app.services.book_service import get_book_or_404


def get_quote_or_404(db: Session, user: User, book: Book, quote_id: int) -> Quote:
    quote = (
        db.query(Quote)
        .filter(Quote.id == quote_id, Quote.user_id == user.id, Quote.book_id == book.id)
        .first()
    )
    if not quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    return quote


def _validate_quote_page(book: Book, page: int | None) -> None:
    if page is not None and page > book.total_pages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quote page cannot be greater than the book total pages",
        )


def list_book_quotes(db: Session, user: User, book_id: int) -> list[Quote]:
    book = get_book_or_404(db, user, book_id)
    return (
        db.query(Quote)
        .options(joinedload(Quote.book))
        .filter(Quote.user_id == user.id, Quote.book_id == book.id)
        .order_by(Quote.created_at.desc())
        .all()
    )


def create_quote(db: Session, user: User, book_id: int, payload: QuoteCreate) -> Quote:
    book = get_book_or_404(db, user, book_id)
    _validate_quote_page(book, payload.page)
    quote = Quote(user_id=user.id, book_id=book.id, **payload.model_dump())
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


def update_quote(db: Session, user: User, book_id: int, quote_id: int, payload: QuoteUpdate) -> Quote:
    book = get_book_or_404(db, user, book_id)
    quote = get_quote_or_404(db, user, book, quote_id)
    fields = payload.model_dump(exclude_unset=True)
    if "page" in fields:
        _validate_quote_page(book, fields["page"])
    for key, value in fields.items():
        setattr(quote, key, value)
    db.commit()
    db.refresh(quote)
    return quote


def delete_quote(db: Session, user: User, book_id: int, quote_id: int) -> None:
    book = get_book_or_404(db, user, book_id)
    quote = get_quote_or_404(db, user, book, quote_id)
    db.delete(quote)
    db.commit()


def list_quotes(db: Session, user: User, search: str | None = None, book_id: int | None = None) -> list[Quote]:
    query = db.query(Quote).options(joinedload(Quote.book)).join(Book).filter(Quote.user_id == user.id)
    if book_id is not None:
        query = query.filter(Quote.book_id == book_id)
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(Quote.text.ilike(pattern), Quote.note.ilike(pattern), Book.title.ilike(pattern)))
    return query.order_by(Quote.created_at.desc()).all()
