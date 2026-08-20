from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class ClubMember(Base):
    # ============================================================
    #  Bảng trung gian club_members
    # Dùng để biểu diễn quan hệ N-N giữa User và Club.
    # ============================================================
    __tablename__ = "club_members"
    # ============================================================
    #  Khóa chính ghép
    # Một user không thể xuất hiện hai lần trong cùng một club.
    # PK = (club_id, user_id)
    # ============================================================
    club_id = Column(Integer,ForeignKey("clubs.id"),primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"),primary_key=True)
  
    # ============================================================
    #  Role của thành viên trong Club
    # OWNER / MEMBER
    # ============================================================
    role = Column(String(20),nullable=False,default="MEMBER")

    # ============================================================
    # Thời gian tham gia
    # ============================================================
    joined_at = Column(DateTime,nullable=False,default=lambda: datetime.now(timezone.utc))

    # ============================================================
    #  Quan hệ ClubMember -> Club
    # ============================================================
    club = relationship("Club",back_populates="members")

    # ============================================================
    #  Quan hệ ClubMember -> User
    # ============================================================
    user = relationship("User",back_populates="club_memberships")
