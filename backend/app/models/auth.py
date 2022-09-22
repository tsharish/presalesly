from email.policy import default
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

from app.db.base import Base

# SQLAlchemy models
class ResourceType(Base):
    __tablename__ = "resource_type"

    id = Column(String, primary_key=True)


class Role(Base):
    id = Column(String, primary_key=True)
    is_reserved = Column(
        Boolean, default=False
    )  # Indicates that the role cannot be assigned to a user. Examples: TECHNNICAL, OWNER, PARENT, GROUP.
    is_standard = Column(Boolean, default=True)  # Indicates an out-of-the-box role


class AccessControl(Base):
    __tablename__ = "access_control"

    id = Column(Integer, primary_key=True)
    resource_type_id = Column(String, ForeignKey("resource_type.id"))
    role_id = Column(String, ForeignKey("role.id"))
    permission = Column(String)
    is_locked = Column(Boolean, default=True)


""" class View(Base):
    id = Column(String, primary_key=True)

#This table will hold the permitted UI Views for each Role
class RoleView(Base):
    __tablename__ = "role_view"

    role_id = Column(String, ForeignKey("role.id"), primary_key=True)
    view_id = Column(String, ForeignKey("view.id"), primary_key=True) """
