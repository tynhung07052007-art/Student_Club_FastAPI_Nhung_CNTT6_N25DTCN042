from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.activity import (
    ActivityCreate,
    ActivityUpdate,
    ActivityResponse
)
from app.core.dependencies import get_current_user
from app.services import activity_service


router = APIRouter(
    # ============================================================
    # THÊM: Router hoạt động Club
    # ============================================================
    prefix="",
    tags=["Club Activities"]
)


@router.post(
    "/clubs/{club_id}/activities",
    response_model=ActivityResponse
)
def create_activity(
    club_id: int,
    data: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return activity_service.create_activity(
        db,
        club_id,
        data,
        current_user
    )


@router.get(
    "/clubs/{club_id}/activities",
    response_model=list[ActivityResponse]
)
def get_activities(
    club_id: int,

    # ============================================================
    # THÊM: Search/filter theo yêu cầu task
    # ============================================================
    search: str | None = Query(None),
    status_filter: str | None = Query(None),
    priority: str | None = Query(None),

    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return activity_service.get_activities(
        db,
        club_id,
        current_user,
        search,
        status_filter,
        priority
    )


@router.get(
    "/activities/{activity_id}",
    response_model=ActivityResponse
)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return activity_service.get_activity(
        db,
        activity_id,
        current_user
    )


@router.patch(
    "/activities/{activity_id}",
    response_model=ActivityResponse
)
def update_activity(
    activity_id: int,
    data: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return activity_service.update_activity(
        db,
        activity_id,
        data,
        current_user
    )


@router.delete(
    "/activities/{activity_id}"
)
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return activity_service.delete_activity(
        db,
        activity_id,
        current_user
    )