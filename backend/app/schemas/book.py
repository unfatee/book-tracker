from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


BookStatus = Literal["want_to_read", "reading", "completed", "paused", "dropped"]


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    genre: str | None = Field(None, max_length=120)
    total_pages: int = Field(..., gt=0)
    current_page: int = Field(0, ge=0)
    status: BookStatus = "want_to_read"
    rating: int | None = Field(None, ge=1, le=5)
    cover_url: str | None = Field(None, max_length=500)
    start_date: date | None = None
    finish_date: date | None = None
    is_favorite: bool = False
    personal_notes: str | None = None


class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    author: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    genre: str | None = Field(None, max_length=120)
    total_pages: int | None = Field(None, gt=0)
    current_page: int | None = Field(None, ge=0)
    status: BookStatus | None = None
    rating: int | None = Field(None, ge=1, le=5)
    cover_url: str | None = Field(None, max_length=500)
    start_date: date | None = None
    finish_date: date | None = None
    is_favorite: bool | None = None
    personal_notes: str | None = None


class BookProgressUpdate(BaseModel):
    current_page: int = Field(..., ge=0)


class BookStatusUpdate(BaseModel):
    status: BookStatus


class BookRead(BaseModel):
    id: int
    user_id: int
    title: str
    author: str
    description: str | None
    genre: str | None
    total_pages: int
    current_page: int
    status: str
    rating: int | None
    cover_url: str | None
    start_date: date | None
    finish_date: date | None
    is_favorite: bool
    personal_notes: str | None
    progress_percent: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
