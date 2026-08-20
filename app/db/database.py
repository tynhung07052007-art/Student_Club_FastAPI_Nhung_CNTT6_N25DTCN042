from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
# ============================================================
#  Lấy DATABASE_URL từ file .env thông qua settings
# Không hard-code username/password database trong code.
# ============================================================
# Chuỗi kết nối MySQL
#  Cú pháp: mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
DATABASE_URL = settings.DATABASE_URL
# ============================================================
# Tạo SQLAlchemy Engine
# Engine chịu trách nhiệm quản lý kết nối tới MySQL.
# ============================================================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
# ============================================================
#  Tạo SessionLocal
# Mỗi request cần làm việc với database sẽ sử dụng một Session.
# ============================================================
# Tạo SessionLocal class, mỗi instance của class này sẽ là một phiên làm việc (session) với database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# ============================================================
#  Base
# Tất cả SQLAlchemy Model sẽ kế thừa Base.
# ============================================================
 # Base class cho tất cả các ORM models
Base = declarative_base()
# ============================================================
#  Dependency get_db
# Tạo database session -> sử dụng -> đóng session.
# finally đảm bảo session luôn được đóng.
# ============================================================
def get_db():
     """
#     Dependency generator để cung cấp database session cho mỗi request.
#     Đảm bảo session được đóng sau khi request hoàn thành (Exception handling scope).
#     """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
