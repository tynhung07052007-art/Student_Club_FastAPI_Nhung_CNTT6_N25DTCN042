from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    # ============================================================
    #  Cấu hình thông tin project
    # ============================================================
    APP_NAME: str = "Student Club Management API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API quản lý câu lạc bộ sinh viên"
    # ============================================================
    #  Cấu hình kết nối MySQL
    # DATABASE_URL được đọc từ file .env
    # ============================================================
    DATABASE_URL: str
    # ============================================================
    #  Cấu hình JWT
    # Chưa làm Login ở Task 1 nhưng chuẩn bị cấu hình
    # theo đúng đặc tả của project.
    # ============================================================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ============================================================
    #  Cấu hình CORS
    # ============================================================
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173"
    ]
    # ============================================================
    # Pydantic Settings V2 sử dụng SettingsConfigDict
    # để đọc file .env.
    # ============================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
# ============================================================
# Tạo một settings dùng chung toàn project.
# Các file khác chỉ cần:
# from app.core.config import settings
# ============================================================
settings = Settings()
