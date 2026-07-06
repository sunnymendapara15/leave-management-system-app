from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, schemas, models
from ..dependencies import get_current_user, get_db

router = APIRouter(prefix="/entitlements", tags=["entitlements"])


@router.get("/", response_model=List[schemas.LeaveEntitlementRead])
def read_entitlements(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
) -> List[schemas.LeaveEntitlementRead]:
    return crud.list_entitlements(db, current_user.id)
