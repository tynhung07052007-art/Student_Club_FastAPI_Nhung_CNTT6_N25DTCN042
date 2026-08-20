from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserResponse
from app.db.database import get_db
from app.core.dependencies import get_current_user, RoleChecker


router = APIRouter(
    # ============================================================
    # THÊM: Router quản lý User
    # ============================================================
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):

    # ============================================================
    # THÊM: User xem thông tin của chính mình
    # ============================================================
    return current_user


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),

    # ============================================================
    # THÊM: Chỉ ADMIN được xem danh sách user
    # ============================================================
    current_user: User = Depends(
        RoleChecker(["admin"])
    )
):

    # ============================================================
    # THÊM: Lấy toàn bộ user
    # ============================================================
    return db.query(User).all()