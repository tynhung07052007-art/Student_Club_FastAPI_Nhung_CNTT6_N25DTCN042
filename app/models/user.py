# from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime, timezone
# from app.db.database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(255), unique=True, index=True, nullable=False)
#     password_hashed = Column(String(255), nullable=False)
#     is_active = Column(Boolean, default=True)

#     # Khóa ngoại: Liên kết tới bảng roles (Quan hệ N-1: Nhiều user có thể cùng 1 role)
#     role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)

from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    # ============================================================
    #  Tạo bảng users
    # ============================================================
    __tablename__ = "users"
    # ============================================================
    #  Khóa chính
    # ============================================================
    id = Column(Integer,primary_key=True,index=True)
    
    # ============================================================
    # Email đăng nhập
    # UNIQUE: Không cho phép hai tài khoản trùng email.
    # ============================================================
    email = Column(String(255),unique=True,index=True,nullable=False)
    # ============================================================
    # Mật khẩu đã hash
    # Không lưu password dạng plain text.
    # ============================================================
    password_hash = Column(String(255),nullable=False)

    # ============================================================
    #  Họ và tên của user
    # ============================================================
    full_name = Column(String(255),nullable=False)
#     # Relationship: Quan hệ 2 chiều với Club
#     # - Chiều xuôi:  owner.club  → lấy object Club của owner đó
#     # - Chiều ngược: club.owner → lấy danh sách tất cả Owner có club đó
#     # back_populates="owners" phải khớp với tên attribute trong class Clubs
#     created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # ============================================================
    #  Role
    # Theo đặc tả: USER / ADMIN.
    # Mặc định USER.
    # ============================================================
    role = Column(String(20),nullable=False,default="USER")
    # ============================================================
    #  Trạng thái tài khoản
    # True = đang hoạt động
    # False = bị vô hiệu hóa
    # ============================================================
    is_active = Column(Boolean,nullable=False,default=True)
    # ============================================================
    #  Thời gian tạo tài khoản
    # ============================================================
    created_at = Column(DateTime,nullable=False,default=lambda: datetime.now(timezone.utc))
    # ============================================================
    #  User 1-N Club
    # Một user có thể sở hữu nhiều câu lạc bộ.
    # ============================================================
    clubs = relationship("Club",back_populates="owner")
    # ============================================================
    #  User N-N Club thông qua ClubMember
    # ============================================================
    club_memberships = relationship("ClubMember",back_populates="user",cascade="all, delete-orphan")
    # ============================================================
    #  User 1-N Activity với vai trò assignee
    # ============================================================
    assigned_activities = relationship("ClubActivity",back_populates="assignee")
