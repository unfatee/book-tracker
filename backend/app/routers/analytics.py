from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.analytics import (
    GenreAnalyticsItem,
    MonthlyReadingItem,
    RecentActivityItem,
    SummaryResponse,
    TopAuthorItem,
)
from app.services import analytics_service
from app.utils.dates import today


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=SummaryResponse)
def summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.get_summary(db, current_user)


@router.get("/by-genre", response_model=list[GenreAnalyticsItem])
def by_genre(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.get_by_genre(db, current_user)


@router.get("/monthly-reading", response_model=list[MonthlyReadingItem])
def monthly_reading(
    year: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return analytics_service.get_monthly_reading(db, current_user, year or today().year)


@router.get("/top-authors", response_model=list[TopAuthorItem])
def top_authors(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.get_top_authors(db, current_user)


@router.get("/recent-activity", response_model=list[RecentActivityItem])
def recent_activity(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return analytics_service.get_recent_activity(db, current_user)
