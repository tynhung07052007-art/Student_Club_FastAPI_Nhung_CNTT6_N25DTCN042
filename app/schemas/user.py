from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ============================================================
# TASK 1 - User Base
# ============================================================
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(
        min_length=2,
        max_length=255
    )


# ============================================================
# TASK 1 - User Create
# Dùng cho dữ liệu tạo user.
# Password chỉ tồn tại ở request, không trả về response.
# ============================================================
class UserCreate(UserBase):
    password: str = Field(
        min_length=6,
        max_length=128
    )
    role: str = "USER"


# ============================================================
# TASK 1 - User Update
# Tất cả field đều optional để sau này hỗ trợ PATCH.
# ============================================================
class UserUpdate(BaseModel):
    email: EmailStr | None = None

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255
    )
    is_active: bool | None = None
    role: str | None = None

# ============================================================
# TASK 1 - User Response
# Không có password/password_hash.
# Đây là điểm quan trọng để không làm lộ mật khẩu.
# ============================================================
class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    # ========================================================
    # TASK 1 - Pydantic đọc trực tiếp SQLAlchemy Model
    # ========================================================
    model_config = ConfigDict(
        from_attributes=True
    )
