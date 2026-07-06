from datetime import date
from typing import List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from . import auth, models, schemas


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    hashed = auth.get_password_hash(user_in.password)
    user = models.User(
        email=user_in.email, full_name=user_in.full_name, hashed_password=hashed
    )
    db.add(user)
    db.flush()
    for leave_type in db.query(models.LeaveType).all():
        ent = models.LeaveEntitlement(
            user_id=user.id,
            leave_type_id=leave_type.id,
            total_days=leave_type.annual_days,
        )
        db.add(ent)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def seed_default_leave_types(db: Session) -> None:
    defaults = [
        ("Annual", "Standard annual leave", 18, True),
        ("Sick", "Sick leave allowance", 12, True),
        ("Casual", "Short-notice personal leave", 6, False),
    ]
    existing = {lt.name.lower() for lt in db.query(models.LeaveType).all()}
    for name, desc, days, requires in defaults:
        if name.lower() not in existing:
            leave_type = models.LeaveType(
                name=name, description=desc, annual_days=days, requires_approval=requires
            )
            db.add(leave_type)
    db.commit()


def create_leave_type(db: Session, leave_in: schemas.LeaveTypeCreate) -> models.LeaveType:
    leave_type = models.LeaveType(**leave_in.dict())
    db.add(leave_type)
    db.flush()
    users = db.query(models.User).all()
    for user in users:
        ent = models.LeaveEntitlement(
            user_id=user.id, leave_type_id=leave_type.id, total_days=leave_type.annual_days
        )
        db.add(ent)
    db.commit()
    db.refresh(leave_type)
    return leave_type


def list_leave_types(db: Session) -> List[models.LeaveType]:
    return db.query(models.LeaveType).order_by(models.LeaveType.name).all()


def get_leave_type(db: Session, leave_type_id: int) -> Optional[models.LeaveType]:
    return db.query(models.LeaveType).filter(models.LeaveType.id == leave_type_id).first()


def update_leave_type(
    db: Session, leave_type: models.LeaveType, patch: schemas.LeaveTypeUpdate
) -> models.LeaveType:
    data = patch.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(leave_type, key, value)
    db.commit()
    db.refresh(leave_type)
    return leave_type


def delete_leave_type(db: Session, leave_type: models.LeaveType) -> None:
    db.delete(leave_type)
    db.commit()


def get_or_create_entitlement(
    db: Session, user_id: int, leave_type: models.LeaveType
) -> models.LeaveEntitlement:
    ent = (
        db.query(models.LeaveEntitlement)
        .filter(
            models.LeaveEntitlement.user_id == user_id,
            models.LeaveEntitlement.leave_type_id == leave_type.id,
        )
        .first()
    )
    if ent:
        return ent
    ent = models.LeaveEntitlement(
        user_id=user_id,
        leave_type_id=leave_type.id,
        total_days=leave_type.annual_days,
    )
    db.add(ent)
    db.commit()
    return ent


def list_entitlements(db: Session, user_id: int) -> List[models.LeaveEntitlement]:
    return (
        db.query(models.LeaveEntitlement)
        .filter(models.LeaveEntitlement.user_id == user_id)
        .join(models.LeaveType)
        .order_by(models.LeaveType.name)
        .all()
    )


def _check_overlapping_request(
    db: Session, user_id: int, start: date, end: date
) -> bool:
    overlap = (
        db.query(models.LeaveRequest)
        .filter(
            models.LeaveRequest.user_id == user_id,
            models.LeaveRequest.status.in_(
                [models.LeaveStatusEnum.pending, models.LeaveStatusEnum.approved]
            ),
            models.LeaveRequest.start_date <= end,
            models.LeaveRequest.end_date >= start,
        )
        .count()
    )
    return overlap > 0


def create_leave_request(
    db: Session, user: models.User, payload: schemas.LeaveRequestCreate
) -> models.LeaveRequest:
    if payload.end_date < payload.start_date:
        raise ValueError("End date must be on or after start date")
    days = (payload.end_date - payload.start_date).days + 1
    leave_type = (
        db.query(models.LeaveType)
        .filter(models.LeaveType.id == payload.leave_type_id)
        .first()
    )
    if not leave_type:
        raise ValueError("Leave type does not exist")
    if _check_overlapping_request(db, user.id, payload.start_date, payload.end_date):
        raise ValueError("Requested dates overlap with another pending or approved leave")
    ent = get_or_create_entitlement(db, user.id, leave_type)
    available = ent.total_days - ent.used_days - ent.reserved_days
    if available < days:
        raise ValueError("Leave balance for this type is insufficient")
    ent.reserved_days += days
    request = models.LeaveRequest(
        user_id=user.id,
        leave_type_id=leave_type.id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        reason=payload.reason,
        requested_days=days,
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def get_leave_requests_for_user(
    db: Session, user_id: int, leave_type_id: Optional[int] = None, status: Optional[str] = None
) -> List[models.LeaveRequest]:
    query = db.query(models.LeaveRequest).filter(models.LeaveRequest.user_id == user_id)
    if leave_type_id:
        query = query.filter(models.LeaveRequest.leave_type_id == leave_type_id)
    if status:
        query = query.filter(models.LeaveRequest.status == status)
    return query.order_by(models.LeaveRequest.start_date.desc()).all()


def list_pending_requests(db: Session, leave_type_id: Optional[int] = None):
    query = db.query(models.LeaveRequest).filter(models.LeaveRequest.status == models.LeaveStatusEnum.pending)
    if leave_type_id:
        query = query.filter(models.LeaveRequest.leave_type_id == leave_type_id)
    return query.order_by(models.LeaveRequest.start_date.asc()).all()


def get_leave_request(db: Session, request_id: int) -> Optional[models.LeaveRequest]:
    return db.query(models.LeaveRequest).filter(models.LeaveRequest.id == request_id).first()


def update_leave_request_status(
    db: Session,
    request: models.LeaveRequest,
    status: str,
    comment: Optional[str] = None,
) -> models.LeaveRequest:
    new_status = models.LeaveStatusEnum(status)
    if request.status != models.LeaveStatusEnum.pending:
        raise ValueError("Only pending requests can be updated")
    ent = (
        db.query(models.LeaveEntitlement)
        .filter(
            models.LeaveEntitlement.user_id == request.user_id,
            models.LeaveEntitlement.leave_type_id == request.leave_type_id,
        )
        .first()
    )
    if not ent:
        raise ValueError("Entitlement missing")
    days = request.requested_days
    ent.reserved_days = max(0, ent.reserved_days - days)
    if new_status == models.LeaveStatusEnum.approved:
        ent.used_days += days
    request.status = new_status
    request.manager_comment = comment
    db.commit()
    db.refresh(request)
    return request
