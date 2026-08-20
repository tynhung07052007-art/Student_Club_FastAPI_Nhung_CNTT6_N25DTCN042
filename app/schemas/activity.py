from pydantic import BaseModel
from datetime import datetime

class ActivityCreate(BaseModel):
    # ============================================================
    # THÊM: Schema tạo hoạt động
    # ============================================================
    title: str
    description: str | None = None
    assignee_id: int | None = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: datetime | None = None

class ActivityUpdate(BaseModel):
    # ============================================================
    # THÊM: PATCH activity
    # ============================================================
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None

class ActivityResponse(BaseModel):

    id: int
    club_id: int
    title: str
    description: str | None = None
    assignee_id: int | None = None
    status: str
    priority: str
    due_date: datetime | None = None
    created_at: datetime

    class Config:
        from_attributes = True