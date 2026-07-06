import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class RoleEnum(str, enum.Enum):
    employee = "employee"
    manager = "manager"
    admin = "admin"


class LeaveStatusEnum(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.employee, nullable=False)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    leave_requests = relationship("LeaveRequest", back_populates="requester")
    entitlements = relationship("LeaveEntitlement", back_populates="user")


class LeaveType(Base):
    __tablename__ = "leave_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    annual_days = Column(Integer, default=0)
    requires_approval = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    requests = relationship("LeaveRequest", back_populates="leave_type")


class LeaveEntitlement(Base):
    __tablename__ = "leave_entitlements"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), primary_key=True)
    total_days = Column(Integer, default=0)
    used_days = Column(Integer, default=0)
    reserved_days = Column(Integer, default=0)

    user = relationship("User", back_populates="entitlements")
    leave_type = relationship("LeaveType")


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=True)
    requested_days = Column(Integer, nullable=False)
    status = Column(Enum(LeaveStatusEnum), default=LeaveStatusEnum.pending, nullable=False)
    manager_comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    requester = relationship("User", back_populates="leave_requests")
    leave_type = relationship("LeaveType", back_populates="requests")
