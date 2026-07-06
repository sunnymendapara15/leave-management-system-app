from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas, models
from ..dependencies import get_db, require_admin

router = APIRouter(prefix="/leave-types", tags=["leave-types"])


@router.get("/", response_model=List[schemas.LeaveTypeRead])
def list_leave_types(db: Session = Depends(get_db)) -> List[schemas.LeaveTypeRead]:
    return crud.list_leave_types(db)


@router.post("/", response_model=schemas.LeaveTypeRead)
def create_leave_type(
    payload: schemas.LeaveTypeCreate, db: Session = Depends(get_db), _: models.User = Depends(require_admin)
) -> schemas.LeaveTypeRead:
    return crud.create_leave_type(db, payload)


@router.put("/{leave_type_id}", response_model=schemas.LeaveTypeRead)
def update_leave_type(
    leave_type_id: int,
    patch: schemas.LeaveTypeUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
) -> schemas.LeaveTypeRead:
    leave_type = crud.get_leave_type(db, leave_type_id)
    if not leave_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found")
    return crud.update_leave_type(db, leave_type, patch)


@router.delete("/{leave_type_id}")
def delete_leave_type(
    leave_type_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    leave_type = crud.get_leave_type(db, leave_type_id)
    if not leave_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found")
    crud.delete_leave_type(db, leave_type)
    return {"detail": "Leave type removed"}
