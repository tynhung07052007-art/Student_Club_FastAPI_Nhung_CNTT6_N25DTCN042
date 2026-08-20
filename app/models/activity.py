from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class ClubActivity(Base):
    __tablename__ = "club_activities"

    # ============================================================
    # THÊM: Khóa chính hoạt động
    # ============================================================
    id = Column(Integer, primary_key=True, index=True)

    # ============================================================
    # THÊM: Hoạt động thuộc Club nào
    # ============================================================
    club_id = Column(
        Integer,
        ForeignKey("clubs.id"),
        nullable=False
    )

    # ============================================================
    # THÊM: Tiêu đề hoạt động
    # ============================================================
    title = Column(
        String(255),
        nullable=False
    )

    # ============================================================
    # THÊM: Mô tả
    # ============================================================
    description = Column(
        Text,
        nullable=True
    )

    # ============================================================
    # THÊM: User được giao xử lý
    # ============================================================
    assignee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    # ============================================================
    # THÊM: Trạng thái hoạt động
    # ============================================================
    status = Column(
        String(30),
        nullable=False,
        default="TODO"
    )

    # ============================================================
    # THÊM: Độ ưu tiên
    # ============================================================
    priority = Column(
        String(30),
        nullable=False,
        default="MEDIUM"
    )

    # ============================================================
    # THÊM: Hạn xử lý
    # ============================================================
    due_date = Column(
        DateTime,
        nullable=True
    )

    # ============================================================
    # THÊM: Ngày tạo
    # ============================================================
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    club = relationship(
        "Club",
        back_populates="activities"
    )

    assignee = relationship(
        "User",
        back_populates="assigned_activities"
    )