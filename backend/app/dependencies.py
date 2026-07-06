from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import auth, crud, models
from .database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    payload = auth.decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = crud.get_user_by_email(db, payload["sub"])
    if not user or user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user


def require_manager(user: models.User = Depends(get_current_user)) -> models.User:
    if user.role not in (models.RoleEnum.manager, models.RoleEnum.admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Manager role required")
    return user


def require_admin(user: models.User = Depends(get_current_user)) -> models.User:
    if user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    return user
