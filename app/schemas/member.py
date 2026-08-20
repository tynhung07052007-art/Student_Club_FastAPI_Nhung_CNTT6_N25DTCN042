from datetime import datetime
from pydantic import BaseModel, ConfigDict

# ============================================================
# TASK 1 - Dữ liệu thêm thành viên
# ============================================================
class ClubMemberCreate(BaseModel):
    user_id: int

# ============================================================
# TASK 1 - Response thành viên
# ============================================================
class ClubMemberResponse(BaseModel):
    club_id: int
    user_id: int
    role: str
    joined_at: datetime
  
    model_config = ConfigDict(
      from_attributes=True
    )
