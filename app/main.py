from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.db.database import Base, engine

# ============================================================
# TASK 1 - Import toàn bộ model.
# Việc import này đảm bảo SQLAlchemy biết:
# User, Club, ClubMember, ClubActivity
# trước khi create_all() chạy.
# ============================================================
from app.models import (
    User,
    Club,
    ClubMember,
    ClubActivity,
)

# ============================================================
# TASK 1 - Khởi tạo FastAPI application
# ============================================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION
)


# ============================================================
# TASK 1 - Cấu hình CORS
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# TASK 1 - Tạo bảng Database
#
# Nếu bảng chưa tồn tại -> SQLAlchemy tạo bảng.
# Nếu bảng đã tồn tại -> giữ nguyên.
#
# Lưu ý:
# Task 1 dùng create_all() để khởi tạo ban đầu.
# ============================================================
Base.metadata.create_all(bind=engine)

# ============================================================
# TASK 1 - Exception 404
#
# Khi endpoint dùng raise HTTPException(404),
# response sẽ có format thống nhất.
# ============================================================
@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail,
            "path": str(request.url.path)
        }
    )


# ============================================================
# TASK 1 - Exception 500
# Đây là lỗi hệ thống ngoài dự kiến.
# Giúp API không trả response lỗi mặc định khó đọc.
# ============================================================
@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "status_code": 500,
            "message": "Internal Server Error",
            "path": str(request.url.path)
        }
    )


# ============================================================
# TASK 1 - Health Check
#
# GET /health
#
# Dùng để kiểm tra FastAPI application có đang chạy hay không.
# ============================================================
@app.get(
    "/health",
    tags=["System"],
    summary="Kiểm tra trạng thái API"
)
def health_check():
    return {
        "success": True,
        "status_code": 200,
        "message": "Student Club Management API is running"
    }

# ============================================================
# TASK 1 - Root endpoint
# ============================================================
@app.get(
    "/",
    tags=["System"],
    summary="Thông tin API"
)
def root():
    return {
        "message": "Student Club Management API",
        "docs": "/docs",
        "health": "/health"
    }
