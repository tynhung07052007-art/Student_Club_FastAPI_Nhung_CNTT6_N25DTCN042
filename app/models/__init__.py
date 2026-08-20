# ============================================================
# TASK 1 - Import toàn bộ model
#
# Khi import các model này, SQLAlchemy sẽ đăng ký các bảng
# vào Base.metadata.
# ============================================================
from app.models.user import User
from app.models.club import Club
from app.models.club_member import ClubMember
from app.models.activity import ClubActivity

__all__ = [
    "User",
    "Club",
    "ClubMember",
    "ClubActivity",
]
