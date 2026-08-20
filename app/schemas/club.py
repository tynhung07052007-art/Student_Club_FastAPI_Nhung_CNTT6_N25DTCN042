from pydantic import BaseModel
from datetime import datetime

class ClubBase(BaseModel):
    # ============================================================
    # THÊM: Thông tin cơ bản của Club
    # ============================================================
    name: str
    description: str | None = None
class ClubCreate(ClubBase):
    pass
class ClubUpdate(BaseModel):
    # ============================================================
    # THÊM: PATCH nên cho phép cập nhật từng trường
    # ============================================================
    name: str | None = None
    description: str | None = None
class ClubResponse(ClubBase):
    id: int
    owner_id: int
    created_at: datetime
    class Config:
        from_attributes = True
class ClubMemberCreate(BaseModel):
    # ============================================================
    # THÊM: Owner dùng user_id để thêm thành viên
    # ============================================================
    user_id: int
class ClubMemberResponse(BaseModel):
    club_id: int
    user_id: int
    role: str
    joined_at: datetime
    class Config:
        from_attributes = True