# ============================================================
# THÊM: Import các model để SQLAlchemy nhận diện đầy đủ
# ============================================================

from app.models.user import User
from app.models.role import Role
from app.models.club import Club, ClubMember
from app.models.activity import ClubActivity