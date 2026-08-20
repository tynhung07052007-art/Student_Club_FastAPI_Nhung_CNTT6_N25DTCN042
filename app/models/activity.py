from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class ClubActivity(Base):
    # ============================================================
    #  Bảng club_activities
    # ============================================================
    __tablename__ = "club_activities"

    # ============================================================
    # TASK 1 - Khóa chính
    # ============================================================
    id = Column(Integer,primary_key=True,index=True)

    # ============================================================
    # TASK 1 - Hoạt động thuộc Club nào
    # FK -> clubs.id
    # ============================================================
    club_id = Column(Integer,ForeignKey("clubs.id"),nullable=False)

    # ============================================================
    # TASK 1 - Tiêu đề hoạt động
    # ============================================================
    title = Column(String(255),nullable=False)

    # ============================================================
    # TASK 1 - Mô tả hoạt động
    # ============================================================
    description = Column(Text,nullable=True)

    # ============================================================
    # TASK 1 - Người được giao hoạt động
    # FK -> users.id
    # Có thể NULL vì hoạt động ban đầu chưa nhất thiết
    # phải được giao cho ai.
    # ============================================================
    assignee_id = Column(IntegerForeignKey("users.id"),nullable=True)

    # ============================================================
    # TASK 1 - Workflow status
    # TODO / IN_PROGRESS / DONE
    # ============================================================
    status = Column(String(30),nullable=False,default="TODO")

    # ============================================================
    # TASK 1 - Priority
    # LOW / MEDIUM / HIGH
    # ============================================================
    priority = Column(String(30),nullable=False,default="MEDIUM")

    # ============================================================
    # TASK 1 - Hạn xử lý
    # ============================================================
    due_date = Column(DateTime,nullable=True)

    # ============================================================
    # TASK 1 - Thời gian tạo
    # ============================================================
    created_at = Column(DateTime,nullable=False,default=lambda: datetime.now(timezone.utc))

    # ============================================================
    # TASK 1 - Quan hệ Activity -> Club
    # ============================================================
    club = relationship("Club",back_populates="activities")

    # ============================================================
    # TASK 1 - Quan hệ Activity -> User assignee
    # ============================================================
    assignee = relationship("User",back_populates="assigned_activities")
