from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.db.database import get_db
from app.services import user_service
from app.core.security import create_access_token


router = APIRouter(
    # ============================================================
    # SỬA: Task yêu cầu /auth/register và /auth/login
    # Không dùng /api/auth
    # ============================================================
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    # ============================================================
    # GIỮ: Gọi service để tạo user
    # ============================================================
    new_user = user_service.create_user(
        db=db,
        user_data=user_data
    )

    return new_user


@router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    # ============================================================
    # GIỮ: Xác thực user
    # ============================================================
    user = user_service.authenticate_user(
        db=db,
        user_data=user_data
    )

    role_name = user.role.name if user.role else None

    # ============================================================
    # GIỮ + SỬA: Tạo JWT
    # ============================================================
    access_token = create_access_token(
        data={
            "sub": user.email,
            "id": user.id,
            "role": role_name
        }
    )

    return {
        "message": "Đăng nhập thành công",
        "access_token": access_token,
        "token_type": "bearer",
        "data": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": role_name,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
    }