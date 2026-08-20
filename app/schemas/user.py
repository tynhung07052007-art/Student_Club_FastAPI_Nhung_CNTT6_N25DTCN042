# from pydantic import BaseModel, EmailStr
# from datetime import datetime
# from app.schemas.role import RoleResponse

# class UserBase(BaseModel):
#     email: EmailStr

# class UserCreate(UserBase):
#     # Dữ liệu đầu vào khi đăng ký: truyền tên role (VD: "user", "admin")
#     password: str
#     role_name: str = "user"  # Mặc định là "user" nếu không truyền vào

# class UserLogin(UserBase):
#     # Dữ liệu đầu vào khi đăng nhập
#     password: str

# class UserResponse(UserBase):
#     # Dữ liệu trả về cho client, TUYỆT ĐỐI KHÔNG trả về mật khẩu
#     id: int
#     is_active: bool
#     # Trả về thông tin role dạng object lồng nhau (nested), không phải chỉ id
#     role: RoleResponse | None = None
#     created_at: datetime

#     class Config:
#         # Pydantic V2 cấu hình từ form_attributes (ở V1 là orm_mode = True)
#         # Giúp Pydantic có thể đọc dữ liệu trực tiếp từ SQLAlchemy Model object
#         from_attributes = True

from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.Role import RoleResponse

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):

    # ============================================================
    # THÊM: Họ tên khi đăng ký
    # ============================================================
    full_name: str

    # ============================================================
    # GIỮ: Password chỉ nhận từ client
    # Sau đó service sẽ hash trước khi lưu DB
    # ============================================================
    password: str
    # ============================================================
    # GIỮ: Role mặc định là user
    # ============================================================
    role_name: str = "user"

class UserLogin(UserBase):

    # ============================================================
    # GIỮ: Password dùng để đăng nhập
    # ============================================================
    password: str

class UserResponse(UserBase):

    id: int

    # ============================================================
    # THÊM: Trả về full_name
    # ============================================================
    full_name: str

    is_active: bool

    role: RoleResponse | None = None

    created_at: datetime

    class Config:
        # GIỮ: Cho phép Pydantic đọc SQLAlchemy object
        from_attributes = True