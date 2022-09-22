from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship, backref, foreign, remote
from sqlalchemy.ext.declarative import declared_attr
from datetime import date, datetime

from app.db.base import Base
from app.models.base import AppBase
from app.models.user import UserTimeStampMixin, UserTimeStampBase
from app.core.enums import Priority, TaskStatus, TaskParentType

# SQLAlchemy models
class Task(Base, UserTimeStampMixin):
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    due_date = Column(Date, nullable=False)
    completed_on = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("user.id"), index=True)
    priority = Column(String, default=Priority.medium)
    is_required = Column(Boolean, default=False)
    status = Column(String, default=TaskStatus.not_started)
    parent_type_id = Column(String, nullable=False)
    parent_id = Column(Integer, nullable=False)

    @property
    def parent(self):
        """Provides in-Python access to the "parent"
        by choosing the appropriate relationship."""
        return getattr(self, "parent_%s" % self.parent_type_id)


# https://docs.sqlalchemy.org/en/14/orm/examples.html#module-examples.generic_associations
class HasTasks(object):
    """HasTasks mixin, creates a new task_association table for each parent."""

    @declared_attr
    def tasks(cls):
        parent_type_id = cls.__tablename__
        task_association = Table(
            "%s_tasks" % cls.__tablename__,
            cls.metadata,
            Column("task_id", ForeignKey("task.id", ondelete="CASCADE"), primary_key=True),
            Column(
                "%s_id" % cls.__tablename__,
                ForeignKey("%s.id" % cls.__tablename__),
                primary_key=True,
            ),
            schema="tenant",
        )
        return relationship(
            Task,
            secondary=task_association,
            backref=backref(
                "parent_%s" % parent_type_id,
                primaryjoin=remote(cls.id) == foreign(Task.parent_id),
                uselist=False,
                viewonly=True,  # This is to prevent UnmappedColumnError
            ),
            cascade="all, delete",  # This will cause all the tasks to be deleted when the parent is deleted
        )


# Pydantic models
class TaskBase(AppBase):
    description: str
    due_date: date
    owner_id: int
    priority: Priority | None = Priority.medium


class TaskCreate(TaskBase):
    status: TaskStatus = TaskStatus.not_started
    parent_type_id: TaskParentType
    parent_id: int


class TaskRead(UserTimeStampBase, TaskBase):
    id: int
    completed_on: datetime | None = None
    is_required: bool
    status: TaskStatus
    parent_type_id: str
    parent_id: int


class TaskUpdate(TaskBase):
    description: str | None = None
    due_date: date | None = None
    owner_id: int | None = None
    status: TaskStatus | None = None
