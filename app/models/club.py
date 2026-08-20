from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base


class Club(Base):
    __tablename__ = "clubs"
    # ============================================================
    # THÊM: Khóa chính Club
    # ============================================================
    id = Column(Integer, primary_key=True, index=True)
    # ============================================================
    # THÊM: Tên câu lạc bộ
    # ============================================================
    name = Column(String(255), nullable=False)
    # ===========================================================
    # THÊM: Mô tả câu lạc bộ
    # ============================================================
    description = Column(Text, nullable=True)
    # ============================================================
    # THÊM: User sở hữu Club
    # ============================================================
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    # ============================================================
    # THÊM: Thời gian tạo Club
    # ============================================================
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    # ============================================================
    # THÊM: Quan hệ Club -> User owner
    # ============================================================
    owner = relationship(
        "User",
        back_populates="clubs"
    )
    # ============================================================
    # THÊM: Một Club có nhiều thành viên
    # ============================================================
    members = relationship(
        "ClubMember",
        back_populates="club",
        cascade="all, delete-orphan"
    )
    # ============================================================
    # THÊM: Một Club có nhiều hoạt động
    # ============================================================
    activities = relationship(
        "ClubActivity",
        back_populates="club",
        cascade="all, delete-orphan"
    )
class ClubMember(Base):
    __tablename__ = "club_members"
    # ============================================================
    # THÊM: Khóa chính của bảng trung gian
    # ============================================================
    club_id = Column(
        Integer,
        ForeignKey("clubs.id"),
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )
    # ============================================================
    # THÊM: OWNER / MEMBER
    # ============================================================
    role = Column(
        String(20),
        nullable=False,
        default="MEMBER"
    )
    # ============================================================
    # THÊM: Thời gian tham gia
    # ============================================================
    joined_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    club = relationship(
        "Club",
        back_populates="members"
    )
    user = relationship(
        "User",
        back_populates="club_memberships"
    )