from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

# ============================================================
# TASK 1 - Club Base
# ============================================================
class ClubBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255
    )
    description: str | None = None

# ============================================================
# TASK 1 - Club Create
# ============================================================
class ClubCreate(ClubBase):
    pass
# ============================================================
# TASK 1 - Club Update
# PATCH nên cho phép cập nhật từng trường.
# ============================================================
class ClubUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )
    description: str | None = None

# ============================================================
# TASK 1 - Club Response
# ============================================================
class ClubResponse(ClubBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
