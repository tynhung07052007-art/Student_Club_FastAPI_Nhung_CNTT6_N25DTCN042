# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.db.database import engine, Base
# from app.routers import member, protected, users
# # Import cả 2 model để SQLAlchemy nhận biết và tạo đủ bảng khi khởi động
# from app.models import club, user  # noqa: F401


# # Khởi tạo ứng dụng FastAPI
# app = FastAPI(
#     title="Demo Authentication FastAPI",
#     description="Ứng dụng mẫu Đăng ký và Đăng nhập với FastAPI và MySQL dành cho sinh viên.",
#     version="1.0.0"
# )

# # Tạo tất cả các bảng trong Database (nếu chưa có)
# # Lưu ý: Trong thực tế dự án lớn thường dùng thư viện Alembic để quản lý database migration thay vì tạo trực tiếp.
# Base.metadata.create_all(bind=engine)

# # ==============================================================================
# # DEMO CORS (Cross-Origin Resource Sharing)
# # ==============================================================================
# # Vấn đề: Trình duyệt (Chrome, Firefox,...) có cơ chế bảo mật gọi là Same-Origin Policy.
# # Mặc định, script trên trang web tại "http://localhost:3000" (React) sẽ BỊ CHẶN
# # nếu cố gắng fetch dữ liệu từ một server khác địa chỉ, ví dụ "http://localhost:8000" (FastAPI).
# # Giải pháp: Server (FastAPI) phải nói cho trình duyệt biết rằng nó cho phép
# # các nguồn (origins) nào được phép gọi tới thông qua CORSMiddleware.
# # ==============================================================================

# # Bước 1: Khai báo danh sách các domain được phép kết nối (Whitelist)
# origins_whitelist = [
#     "http://localhost:3000",             # Môi trường phát triển của Frontend React/Vue
#     "http://localhost:5173",             # Môi trường phát triển của Frontend Vite
#     "https://admin.myapp.com",          # Hệ thống quản trị nội bộ trên Production
#     "https://myapp.com",                # Trang chủ chính thức
# ]

# # Bước 2: Tích hợp CORSMiddleware vào ứng dụng (tầng Global - áp dụng cho TẤT CẢ endpoint)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins_whitelist,     # Chỉ cho phép các nguồn trong danh sách trắng
#                                          # (Dùng ["*"] để cho phép tất cả - KHÔNG nên dùng trên Production!)
#     allow_credentials=True,             # Cho phép Client gửi kèm Cookies / Authorization Headers
#     allow_methods=["GET", "POST", "PUT", "DELETE"],  # Giới hạn các phương thức được phép
#     allow_headers=["Content-Type", "Authorization"], # Giới hạn các Header được gửi lên
# )

# # Nhúng router xử lý auth vào ứng dụng chính
# app.include_router(member.router)

# # Nhúng router xử lý các API cần xác thực (Authorization)
# app.include_router(protected.router)

# # Nhúng router demo CORS
# app.include_router(users.router)

# @app.get("/health")
# def health_check():
#     return {
#         "status": "success",
#         "message": "Student Club Management API"
#     }

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import engine, Base

# ============================================================
# THÊM: Import toàn bộ model để SQLAlchemy biết các bảng
# ============================================================
from app.models import user
from app.models import role
from app.models import club
from app.models import activity

# ============================================================
# THÊM: Import các router chính của project
# ============================================================
from app.routers import auth
from app.routers import users
from app.routers import clubs
from app.routers import activities


app = FastAPI(
    # ============================================================
    # SỬA: Thông tin project
    # ============================================================
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION
)


# ============================================================
# GIỮ: Tạo bảng database nếu chưa tồn tại
# ============================================================
Base.metadata.create_all(bind=engine)


# ============================================================
# THÊM: Cấu hình CORS
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# THÊM: Router Authentication
# POST /auth/register
# POST /auth/login
# ============================================================
app.include_router(auth.router)


# ============================================================
# THÊM: Router User
# GET /users/me
# GET /users
# ============================================================
app.include_router(users.router)


# ============================================================
# THÊM: Router Club
# /clubs
# ============================================================
app.include_router(clubs.router)


# ============================================================
# THÊM: Router Activity
# /clubs/{club_id}/activities
# /activities/{activity_id}
# ============================================================
app.include_router(activities.router)


# ============================================================
# THÊM: Health-check endpoint
#
# Không cần tạo health.py.
# Task chỉ yêu cầu có health-check endpoint.
# ============================================================
@app.get("/health")
def health_check():

    return {
        "status": "success",
        "message": "Student Club Management API is running"
    }


# ============================================================
# GIỮ + SỬA: Root endpoint
# ============================================================
@app.get("/")
def root():

    return {
        "message": "Student Club Management API",
        "docs": "/docs",
        "health": "/health"
    }