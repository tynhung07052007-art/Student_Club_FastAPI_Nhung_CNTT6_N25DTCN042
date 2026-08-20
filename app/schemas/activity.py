from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# TASK 1 - Activity Base
# ============================================================
class ActivityBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = None
    assignee_id: int | None = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: datetime | None = None
    
# ============================================================
# TASK 1 - Activity Create
# ============================================================
class ActivityCreate(ActivityBase):
    pass
# ============================================================
# TASK 1 - Activity Update
# PATCH:
# Chỉ những trường được gửi lên mới được cập nhật.
# ============================================================
class ActivityUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = None
    assignee_id: int | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None

# ============================================================
# TASK 1 - Activity Response
# ============================================================
class ActivityResponse(BaseModel):
    id: int
    club_id: int
    title: str
    description: str | None
    assignee_id: int | None
    status: str
    priority: str
    due_date: datetime | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
