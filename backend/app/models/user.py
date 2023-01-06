from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import (
    relationship,
    declarative_mixin,
    declared_attr,
    column_property,
)
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.db.base import Base
from app.models.base import AppBase

# SQLAlchemy models
@declarative_mixin
class UserTimeStampMixin:
    """Provides created and last modified user and date time stamp info for objects"""

    created_on = Column(DateTime, server_default=func.now())
    created_on._creation_order = 9997  # type: ignore
    # Columns with foreign keys to other columns must be declared as @declared_attr callables on declarative mixin classes.
    # Refer to 'Composing Mapped Hierarchies with Mixins' in SQLAlchemy documentation.
    @declared_attr
    def created_by_id(cls):
        return Column("created_by_id", ForeignKey("user.id"))

    @declared_attr
    def created_by(cls):
        return relationship("User", primaryjoin=lambda: User.id == cls.created_by_id)

    updated_on = Column(DateTime, server_onupdate=func.now())
    updated_on._creation_order = 9998  # type: ignore

    @declared_attr
    def updated_by_id(cls):
        return Column("updated_by_id", ForeignKey("user.id"))

    @declared_attr
    def updated_by(cls):
        return relationship("User", primaryjoin=lambda: User.id == cls.updated_by_id)


# The User class does not use the UserTimeStampMixin as it was not able to create the relationships correctly (possibly due to self-referencing).
# The following (using remote_side) is the proper way. Refer to 'Adjacency List Relationships' in SQLAlchemy documentation.
class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)  # Password hash
    first_name = Column(String)
    last_name = Column(String)
    employee_id = Column(String)
    language_code = Column(String, ForeignKey("shared.language.code"), default="EN")
    last_login_date_time = Column(DateTime)
    last_password_changed_on = Column(DateTime)
    failed_logins = Column(Integer)
    role_id = Column(String, ForeignKey("role.id"))
    is_active = Column(Boolean, default=True)
    is_initial_password = Column(Boolean, default=True)
    created_on = Column(DateTime, default=func.now())
    created_by_id = Column(Integer, ForeignKey("user.id"))
    updated_on = Column(DateTime, onupdate=func.now())
    updated_by_id = Column(Integer, ForeignKey("user.id"))
    created_by = relationship("User", remote_side=[id], foreign_keys=[created_by_id])
    updated_by = relationship("User", remote_side=[id], foreign_keys=[updated_by_id])
    # Without remote_side, Pydantic throws this error: response -> items -> 0 -> created_by -> email. field required (type=value_error.missing)
    # Without foreign_keys, AmbiguousForeignKeysError is raised since SQLAlchemy does not know which foreign key to use for the join
    full_name = column_property(first_name + " " + last_name)

    @classmethod
    def get_resource_type(cls):
        return "setting"


# Pydantic models
class UserBase(AppBase):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    employee_id: str | None = None


class UserSummary(UserBase):
    id: int
    full_name: str | None = None


class UserDetail(UserBase):
    language_code: str | None = "EN"
    role_id: str


class UserCreate(UserDetail):
    password: str


class UserTimeStampBase(BaseModel):
    """User Timestamp info to be included in other models"""

    created_by: UserSummary | None = None
    updated_by: UserSummary | None = None
    created_on: datetime | None = None
    updated_on: datetime | None = None


class UserRead(UserTimeStampBase, UserDetail):
    id: int
    full_name: str | None = None


class UserUpdate(UserDetail):
    email: EmailStr | None = None
    role_id: str | None = None


class UserPasswordUpdate(AppBase):
    password: str
