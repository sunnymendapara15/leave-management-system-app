from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import crud, schemas, models
from ..dependencies import get_current_user, get_db, require_manager

router = APIRouter(prefix="/leave-requests", tags=["leave-requests"])


@router.get("/", response_model=List[schemas.LeaveRequestRead])
def read_my_requests(
    leave_type_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> List[schemas.LeaveRequestRead]:
    return crud.get_leave_requests_for_user(db, current_user.id, leave_type_id, status)


@router.post("/", response_model=schemas.LeaveRequestRead)
def submit_leave_request(
    payload: schemas.LeaveRequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> schemas.LeaveRequestRead:
    try:
        return crud.create_leave_request(db, current_user, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/pending", response_model=List[schemas.LeaveRequestRead])
def list_pending_requests(
    leave_type_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _: models.User = Depends(require_manager),
) -> List[schemas.LeaveRequestRead]:
    return crud.list_pending_requests(db, leave_type_id)


@router.patch("/{request_id}/status", response_model=schemas.LeaveRequestRead)
def update_status(
    request_id: int,
    payload: schemas.LeaveRequestStatusUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_manager),
) -> schemas.LeaveRequestRead:
    request = crud.get_leave_request(db, request_id)
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found")
    try:
        return crud.update_leave_request_status(db, request, payload.status, payload.manager_comment)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
