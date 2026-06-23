from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.reading_goal import (
    ReadingGoalCreate,
    ReadingGoalProgress,
    ReadingGoalRead,
    ReadingGoalUpdate,
)
from app.services import goal_service


router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("", response_model=list[ReadingGoalRead])
@router.get("/", response_model=list[ReadingGoalRead], include_in_schema=False)
def get_goals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return goal_service.list_goals(db, current_user)


@router.post("", response_model=ReadingGoalRead, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=ReadingGoalRead, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_goal(
    payload: ReadingGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return goal_service.create_or_update_goal(db, current_user, payload)


@router.get("/{year}", response_model=ReadingGoalRead)
def get_goal(year: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return goal_service.get_goal_or_404(db, current_user, year)


@router.put("/{year}", response_model=ReadingGoalRead)
def update_goal(
    year: int,
    payload: ReadingGoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return goal_service.update_goal(db, current_user, year, payload)


@router.delete("/{year}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(year: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    goal_service.delete_goal(db, current_user, year)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{year}/progress", response_model=ReadingGoalProgress)
def goal_progress(year: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return goal_service.get_goal_progress(db, current_user, year)
