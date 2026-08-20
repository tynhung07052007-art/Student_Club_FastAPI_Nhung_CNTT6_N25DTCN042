from app.db.database import Base, engine

# ============================================================
# TASK 1 - Import model để SQLAlchemy đăng ký đầy đủ
# các bảng trước khi create_all().
# ============================================================
from app.models import (
    User,
    Club,
    ClubMember,
    ClubActivity,
)

def init_db():
    # ========================================================
    # TASK 1 - Tạo các bảng nếu chưa tồn tại.
    # ========================================================
    Base.metadata.create_all(bind=engine)

    print("Database tables initialized successfully.")

if __name__ == "__main__":
    init_db()
