# from sqlalchemy.orm import Session
# from fastapi import HTTPException, status
# from app.models.user import User
# from app.models.club import Role
# from app.schemas.user import UserCreate, UserLogin
# from app.core.security import hash_password, verify_password

# def create_user(db: Session, user_data: UserCreate):
#     """
#     Logic Đăng ký tài khoản:
#     1. Kiểm tra xem email đã tồn tại trong database chưa.
#     2. Nếu tồn tại, ném ra lỗi HTTPException (400 Bad Request).
#     3. Tìm kiếm role theo tên (role_name) trong bảng roles.
#     4. Băm mật khẩu người dùng.
#     5. Lưu thông tin người dùng (với role_id và mật khẩu đã băm) vào database.
#     """
#     # 1. Kiểm tra email tồn tại
#     existing_user = db.query(User).filter(User.email == user_data.email).first()
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email đã tồn tại"
#         )

#     # 2. Tìm role theo tên trong bảng roles
#     role = db.query(Role).filter(Role.name == user_data.role_name).first()
#     if not role:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Vai trò '{user_data.role_name}' không tồn tại trong hệ thống!"
#         )

#     # 3. Băm mật khẩu bằng helper
#     hashed_pwd = hash_password(user_data.password)

#     # 4. Tạo User model instance mới, gán role_id (khóa ngoại) thay vì chuỗi role
#     new_user = User(
#         email=user_data.email,
#         hashed_password=hashed_pwd,
#         role_id=role.id  # Liên kết tới bảng roles qua khóa ngoại
#     )

#     # 5. Thêm vào session và lưu xuống DB
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)  # Cập nhật lại new_user với thông tin lấy từ DB

#     return new_user

# def authenticate_user(db: Session, user_data: UserLogin):
#     """
#     Logic Đăng nhập:
#     1. Tìm người dùng trong database theo email.
#     2. Nếu không tìm thấy, hoặc nếu có mà mật khẩu không khớp -> lỗi 400.
#     3. Trả về thông tin người dùng nếu thành công.
#     """
#     # 1. Tìm user theo email
#     user = db.query(User).filter(User.email == user_data.email).first()

#     # 2. Kiểm tra user có tồn tại không VÀ mật khẩu có khớp không
#     if not user or not verify_password(user_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email hoặc mật khẩu không chính xác"
#         )

#     # 3. Đăng nhập thành công, trả về model user
#     return user

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_password, verify_password


def create_user(db: Session, user_data: UserCreate):

    # ============================================================
    # GIỮ: Kiểm tra email đã tồn tại
    # ============================================================
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email đã tồn tại"
        )

    # ============================================================
    # GIỮ: Tìm role
    # ============================================================
    role = db.query(Role).filter(
        Role.name == user_data.role_name
    ).first()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vai trò '{user_data.role_name}' không tồn tại"
        )

    # ============================================================
    # GIỮ: Hash password trước khi lưu
    # ============================================================
    password_hash = hash_password(user_data.password)

    # ============================================================
    # SỬA: Tạo User theo schema mới
    # ============================================================
    new_user = User(
        email=user_data.email,
        password_hash=password_hash,
        full_name=user_data.full_name,
        role_id=role.id,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, user_data: UserLogin):

    # ============================================================
    # GIỮ: Tìm user theo email
    # ============================================================
    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    # ============================================================
    # SỬA: Đổi hashed_password -> password_hash
    # ============================================================
    if not user or not verify_password(
        user_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email hoặc mật khẩu không chính xác"
        )

    return user