from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str]
    role: Optional[str]


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str]


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True


class LeaveTypeBase(BaseModel):
    name: str
    description: Optional[str]
    annual_days: int
    requires_approval: bool = True


class LeaveTypeCreate(LeaveTypeBase):
    pass


class LeaveTypeUpdate(BaseModel):
    description: Optional[str]
    annual_days: Optional[int]
    requires_approval: Optional[bool]


class LeaveTypeRead(LeaveTypeBase):
    id: int

    class Config:
        orm_mode = True


class LeaveEntitlementRead(BaseModel):
    leave_type: LeaveTypeRead
    total_days: int
    used_days: int
    reserved_days: int

    class Config:
        orm_mode = True


class LeaveRequestBase(BaseModel):
    leave_type_id: int
    start_date: date
    end_date: date
    reason: Optional[str]


class LeaveRequestCreate(LeaveRequestBase):
    pass


class LeaveRequestStatusUpdate(BaseModel):
    status: str
    manager_comment: Optional[str]


class LeaveRequestRead(LeaveRequestBase):
    id: int
    requested_days: int
    status: str
    manager_comment: Optional[str]
    leave_type: LeaveTypeRead
    requester: UserRead

    class Config:
        orm_mode = True


class ProfileResponse(UserRead):
    pass
