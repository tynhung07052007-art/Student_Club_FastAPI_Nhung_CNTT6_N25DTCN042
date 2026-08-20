from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.club import ClubMember
from app.schemas.club import (
    ClubCreate,
    ClubUpdate,
    ClubResponse,
    ClubMemberCreate,
    ClubMemberResponse
)
from app.core.dependencies import get_current_user
from app.services import club_service


router = APIRouter(
    # ============================================================
    # THÊM: Router quản lý Club
    # ============================================================
    prefix="/clubs",
    tags=["Clubs"]
)


@router.post(
    "",
    response_model=ClubResponse,
    status_code=status.HTTP_201_CREATED
)
def create_club(
    club_data: ClubCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return club_service.create_club(
        db,
        club_data,
        current_user
    )


@router.get(
    "",
    response_model=list[ClubResponse]
)
def get_my_clubs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return club_service.get_my_clubs(
        db,
        current_user
    )


@router.get(
    "/{club_id}",
    response_model=ClubResponse
)
def get_club(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return club_service.get_club(
        db,
        club_id,
        current_user
    )


@router.patch(
    "/{club_id}",
    response_model=ClubResponse
)
def update_club(
    club_id: int,
    club_data: ClubUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return club_service.update_club(
        db,
        club_id,
        club_data,
        current_user
    )


@router.delete(
    "/{club_id}"
)
def delete_club(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return club_service.delete_club(
        db,
        club_id,
        current_user
    )


@router.post(
    "/{club_id}/members",
    response_model=ClubMemberResponse,
    status_code=status.HTTP_201_CREATED
)
def add_member(
    club_id: int,
    member_data: ClubMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ============================================================
    # THÊM: Chỉ Owner được thêm thành viên
    # ============================================================
    if not club_service.is_owner(
        db,
        club_id,
        current_user.id
    ):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="Chỉ Owner mới được thêm thành viên"
        )

    # ============================================================
    # THÊM: Kiểm tra user cần thêm có tồn tại không
    # ============================================================
    user = db.query(User).filter(
        User.id == member_data.user_id
    ).first()

    if not user:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Người dùng không tồn tại"
        )

    # ============================================================
    # THÊM: Không cho thêm thành viên trùng
    # ============================================================
    existing = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == member_data.user_id
    ).first()

    if existing:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400,
            detail="Người dùng đã là thành viên"
        )

    member = ClubMember(
        club_id=club_id,
        user_id=member_data.user_id,
        role="MEMBER"
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


@router.get(
    "/{club_id}/members",
    response_model=list[ClubMemberResponse]
)
def get_members(
    club_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ============================================================
    # THÊM: Chỉ Member của Club mới được xem danh sách
    # ============================================================
    if not club_service.is_member(
        db,
        club_id,
        current_user.id
    ):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="Bạn không phải thành viên của câu lạc bộ"
        )

    return db.query(ClubMember).filter(
        ClubMember.club_id == club_id
    ).all()


@router.delete(
    "/{club_id}/members/{user_id}"
)
def remove_member(
    club_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ============================================================
    # THÊM: Chỉ Owner được xóa thành viên
    # ============================================================
    if not club_service.is_owner(
        db,
        club_id,
        current_user.id
    ):
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="Chỉ Owner mới được xóa thành viên"
        )

    member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == user_id
    ).first()

    if not member:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Thành viên không tồn tại"
        )

    # ============================================================
    # THÊM: Không cho Owner tự xóa chính mình
    # ============================================================
    if member.role == "OWNER":
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400,
            detail="Không thể xóa Owner khỏi câu lạc bộ"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Xóa thành viên thành công"
    }