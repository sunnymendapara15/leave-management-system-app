from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import auth, crud, schemas
from ..dependencies import get_db, get_current_user

router = APIRouter()


@router.post("/auth/register", response_model=schemas.UserRead)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserRead:
    try:
        user = crud.create_user(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return user


@router.post("/auth/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)) -> schemas.Token:
    user = crud.get_user_by_email(db, payload.email)
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    token = auth.create_access_token({"sub": user.email, "role": user.role.value})
    return schemas.Token(access_token=token)


@router.get("/users/me", response_model=schemas.UserRead)
def read_profile(current_user=Depends(get_current_user)) -> schemas.UserRead:
    return current_user
