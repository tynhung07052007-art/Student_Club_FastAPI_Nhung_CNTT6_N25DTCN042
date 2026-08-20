# from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     # --- Cấu hình ứng dụng ---
#     APP_NAME: str = "Demo FastAPI"
#     APP_VERSION: str = "1.0.0"
#     APP_DESCRIPTION: str = "Ứng dụng mẫu Authentication & Authorization với FastAPI."

#     # --- Cấu hình Database ---
#     # Đọc từ biến môi trường DATABASE_URL trong file .env
#     DATABASE_URL: str

#     # --- Cấu hình JWT ---
#     # Đọc từ biến môi trường SECRET_KEY trong file .env
#     SECRET_KEY: str
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

#     # --- Cấu hình CORS ---
#     # Đọc từ biến môi trường ALLOWED_ORIGINS trong file .env (dạng JSON list)
#     ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

#     class Config:
#         # Chỉ định file .env để pydantic-settings tự động đọc
#         env_file = ".env"
#         env_file_encoding = "utf-8"


# # Khởi tạo một instance duy nhất (Singleton) dùng cho toàn bộ ứng dụng
# # Các file khác chỉ cần: from app.core.config import settings
# settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ============================================================
    # SỬA: Cấu hình tên project Student Club Management
    # ============================================================
    APP_NAME: str = "Student Club Management API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API quản lý câu lạc bộ sinh viên"

    # ============================================================
    # GIỮ: Đọc DATABASE_URL từ file .env
    # ============================================================
    DATABASE_URL: str

    # ============================================================
    # GIỮ: Cấu hình JWT
    # ============================================================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ============================================================
    # THÊM: Cho phép cấu hình CORS từ .env
    # ============================================================
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173"
    ]

    class Config:
        # GIỮ: Đọc cấu hình từ file .env
        env_file = ".env"
        env_file_encoding = "utf-8"


# GIỮ: Tạo một settings dùng chung cho toàn project
settings = Settings()