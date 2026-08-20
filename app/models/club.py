from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base


class Club(Base):
    # ============================================================
    # Tạo Bảng clubs
    # ============================================================
    __tablename__ = "clubs"

    # ============================================================
    # Khóa chính
    # ============================================================
    id = Column(Integer,primary_key=True,index=True)

    # ============================================================
    #  Tên câu lạc bộ
    # ============================================================
    name = Column(String(255),nullable=False)
    # ============================================================
    #  Mô tả câu lạc bộ
    # ============================================================
    description = Column(Text,nullable=True)
    # ============================================================
    # Người sở hữu câu lạc bộ
    # FK -> users.id
    # ============================================================
    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    # ============================================================
    #  Thời gian tạo
    # ============================================================
    created_at = Column(DateTime,nullable=False,default=lambda: datetime.now(timezone.utc))

    # ============================================================
    #  Quan hệ Club -> User owner
    # ============================================================
    owner = relationship("User",back_populates="clubs")

    # ============================================================
    #  Club 1-N ClubMember
    # ============================================================
    members = relationship("ClubMember",back_populates="club",cascade="all, delete-orphan")

    # ============================================================
    #  Club 1-N ClubActivity
    # ============================================================
    activities = relationship("ClubActivity",back_populates="club",cascade="all, delete-orphan")
