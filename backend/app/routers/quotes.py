from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.quote import QuoteCreate, QuoteRead, QuoteUpdate
from app.services import quote_service


router = APIRouter(tags=["quotes"])


@router.get("/books/{book_id}/quotes", response_model=list[QuoteRead])
def get_book_quotes(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return quote_service.list_book_quotes(db, current_user, book_id)


@router.post("/books/{book_id}/quotes", response_model=QuoteRead, status_code=status.HTTP_201_CREATED)
def create_quote(
    book_id: int,
    payload: QuoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return quote_service.create_quote(db, current_user, book_id, payload)


@router.put("/books/{book_id}/quotes/{quote_id}", response_model=QuoteRead)
def update_quote(
    book_id: int,
    quote_id: int,
    payload: QuoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return quote_service.update_quote(db, current_user, book_id, quote_id, payload)


@router.delete("/books/{book_id}/quotes/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quote(
    book_id: int,
    quote_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    quote_service.delete_quote(db, current_user, book_id, quote_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/quotes", response_model=list[QuoteRead])
def get_quotes(
    search: str | None = None,
    book_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return quote_service.list_quotes(db, current_user, search=search, book_id=book_id)
