from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.activity import ClubActivity
from app.models.user import User
from app.models.club import ClubMember
from app.schemas.activity import ActivityCreate, ActivityUpdate


def check_member(
    db: Session,
    club_id: int,
    user_id: int
):

    # ============================================================
    # THÊM: Kiểm tra user có phải Member của Club không
    # ============================================================
    member = db.query(ClubMember).filter(
        ClubMember.club_id == club_id,
        ClubMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của câu lạc bộ"
        )

    return member


def create_activity(
    db: Session,
    club_id: int,
    data: ActivityCreate,
    current_user: User
):

    check_member(
        db,
        club_id,
        current_user.id
    )

    # ============================================================
    # THÊM: Nếu có assignee thì phải kiểm tra người đó là member
    # ============================================================
    if data.assignee_id:

        assignee = db.query(ClubMember).filter(
            ClubMember.club_id == club_id,
            ClubMember.user_id == data.assignee_id
        ).first()

        if not assignee:
            raise HTTPException(
                status_code=400,
                detail="Người được giao phải là thành viên của câu lạc bộ"
            )

    activity = ClubActivity(
        club_id=club_id,
        title=data.title,
        description=data.description,
        assignee_id=data.assignee_id,
        status=data.status,
        priority=data.priority,
        due_date=data.due_date
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def get_activities(
    db: Session,
    club_id: int,
    current_user: User,
    search: str | None = None,
    status_filter: str | None = None,
    priority: str | None = None
):

    check_member(
        db,
        club_id,
        current_user.id
    )

    query = db.query(ClubActivity).filter(
        ClubActivity.club_id == club_id
    )

    # ============================================================
    # THÊM: Search theo title
    # ============================================================
    if search:
        query = query.filter(
            ClubActivity.title.ilike(f"%{search}%")
        )

    # ============================================================
    # THÊM: Filter status
    # ============================================================
    if status_filter:
        query = query.filter(
            ClubActivity.status == status_filter
        )

    # ============================================================
    # THÊM: Filter priority
    # ============================================================
    if priority:
        query = query.filter(
            ClubActivity.priority == priority
        )

    return query.all()


def get_activity(
    db: Session,
    activity_id: int,
    current_user: User
):

    activity = db.query(ClubActivity).filter(
        ClubActivity.id == activity_id
    ).first()

    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Hoạt động không tồn tại"
        )

    check_member(
        db,
        activity.club_id,
        current_user.id
    )

    return activity


def update_activity(
    db: Session,
    activity_id: int,
    data: ActivityUpdate,
    current_user: User
):

    activity = get_activity(
        db,
        activity_id,
        current_user
    )

    # ============================================================
    # THÊM: Owner hoặc assignee được cập nhật
    # ============================================================
    member = check_member(
        db,
        activity.club_id,
        current_user.id
    )

    if (
        member.role != "OWNER"
        and activity.assignee_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền cập nhật hoạt động này"
        )

    # ============================================================
    # THÊM: Cập nhật từng trường được gửi lên
    # ============================================================
    if data.title is not None:
        activity.title = data.title

    if data.description is not None:
        activity.description = data.description

    if data.status is not None:
        activity.status = data.status

    if data.priority is not None:
        activity.priority = data.priority

    if data.due_date is not None:
        activity.due_date = data.due_date

    if data.assignee_id is not None:

        assignee = db.query(ClubMember).filter(
            ClubMember.club_id == activity.club_id,
            ClubMember.user_id == data.assignee_id
        ).first()

        if not assignee:
            raise HTTPException(
                status_code=400,
                detail="Assignee phải là thành viên của Club"
            )

        activity.assignee_id = data.assignee_id

    db.commit()
    db.refresh(activity)

    return activity


def delete_activity(
    db: Session,
    activity_id: int,
    current_user: User
):

    activity = get_activity(
        db,
        activity_id,
        current_user
    )

    member = check_member(
        db,
        activity.club_id,
        current_user.id
    )

    # ============================================================
    # THÊM: Chỉ Owner được xóa activity
    # ============================================================
    if member.role != "OWNER":
        raise HTTPException(
            status_code=403,
            detail="Chỉ Owner mới được xóa hoạt động"
        )

    db.delete(activity)
    db.commit()

    return {
        "message": "Xóa hoạt động thành công"
    }