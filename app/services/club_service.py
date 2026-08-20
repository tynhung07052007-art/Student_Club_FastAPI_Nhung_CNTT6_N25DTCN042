from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.club import Club, ClubMember
from app.models.user import User
from app.schemas.club import ClubCreate, ClubUpdate


def is_member(
    db: Session,
    club_id: int,
    user_id: int
):

    # ============================================================
    # THÊM: Kiểm tra user có thuộc Club hay không
    # ============================================================
    return db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == user_id
    ).first()


def is_owner(
    db: Session,
    club_id: int,
    user_id: int
):

    # ============================================================
    # THÊM: Kiểm tra user có phải Owner hay không
    # ============================================================
    club = db.query(Club).filter(
        Club.id == club_id
    ).first()

    if not club:
        return False

    return club.owner_id == user_id


def create_club(
    db: Session,
    club_data: ClubCreate,
    current_user: User
):

    # ============================================================
    # THÊM: Tạo Club với current_user là owner
    # ============================================================
    club = Club(
        name=club_data.name,
        description=club_data.description,
        owner_id=current_user.id
    )

    db.add(club)
    db.commit()
    db.refresh(club)

    # ============================================================
    # THÊM: Owner cũng được lưu vào bảng club_members
    # ============================================================
    owner_member = ClubMember(
        club_id=club.id,
        user_id=current_user.id,
        role="OWNER"
    )

    db.add(owner_member)
    db.commit()

    return club


def get_my_clubs(
    db: Session,
    current_user: User
):

    # ============================================================
    # THÊM: Lấy các Club mà user tham gia
    # ============================================================
    return (
        db.query(Club)
        .join(ClubMember)
        .filter(
            ClubMember.user_id == current_user.id
        )
        .all()
    )


def get_club(
    db: Session,
    club_id: int,
    current_user: User
):

    club = db.query(Club).filter(
        Club.id == club_id
    ).first()

    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Câu lạc bộ không tồn tại"
        )

    # ============================================================
    # THÊM: Endpoint yêu cầu Member
    # ============================================================
    member = is_member(
        db,
        club_id,
        current_user.id
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của câu lạc bộ"
        )

    return club


def update_club(
    db: Session,
    club_id: int,
    club_data: ClubUpdate,
    current_user: User
):

    # ============================================================
    # THÊM: Chỉ Owner được sửa Club
    # ============================================================
    if not is_owner(
        db,
        club_id,
        current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ Owner mới được cập nhật câu lạc bộ"
        )

    club = db.query(Club).filter(
        Club.id == club_id
    ).first()

    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Câu lạc bộ không tồn tại"
        )

    if club_data.name is not None:
        club.name = club_data.name

    if club_data.description is not None:
        club.description = club_data.description

    db.commit()
    db.refresh(club)

    return club


def delete_club(
    db: Session,
    club_id: int,
    current_user: User
):

    # ============================================================
    # THÊM: Chỉ Owner được xóa Club
    # ============================================================
    if not is_owner(
        db,
        club_id,
        current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ Owner mới được xóa câu lạc bộ"
        )

    club = db.query(Club).filter(
        Club.id == club_id
    ).first()

    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Câu lạc bộ không tồn tại"
        )

    db.delete(club)
    db.commit()

    return {
        "message": "Xóa câu lạc bộ thành công"
    }