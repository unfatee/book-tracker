from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.book import BookCreate, BookProgressUpdate, BookRead, BookStatusUpdate, BookUpdate
from app.services import book_service


router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[BookRead])
@router.get("/", response_model=list[BookRead], include_in_schema=False)
def get_books(
    status_filter: str | None = Query(None, alias="status"),
    genre: str | None = None,
    rating: int | None = Query(None, ge=1, le=5),
    is_favorite: bool | None = None,
    search: str | None = None,
    sort_by: str = "updated_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return book_service.list_books(
        db,
        current_user,
        status_filter=status_filter,
        genre=genre,
        rating=rating,
        is_favorite=is_favorite,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_book(
    payload: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return book_service.create_book(db, current_user, payload)


@router.post("/demo-data", response_model=list[BookRead], status_code=status.HTTP_201_CREATED)
def create_demo_data(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return book_service.create_demo_data(db, current_user)


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return book_service.get_book_or_404(db, current_user, book_id)


@router.put("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    payload: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return book_service.update_book(db, current_user, book_id, payload)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book_service.delete_book(db, current_user, book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{book_id}/progress", response_model=BookRead)
def update_progress(
    book_id: int,
    payload: BookProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return book_service.update_progress(db, current_user, book_id, payload)


@router.patch("/{book_id}/favorite", response_model=BookRead)
def toggle_favorite(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return book_service.toggle_favorite(db, current_user, book_id)


@router.patch("/{book_id}/status", response_model=BookRead)
def update_status(
    book_id: int,
    payload: BookStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return book_service.update_status(db, current_user, book_id, payload)
