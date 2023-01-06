from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from datetime import date, datetime

from app.db.base import Base
from app.models.base import AppBase
from app.models.user import UserTimeStampMixin, UserTimeStampBase, UserSummary
from app.core.enums import Priority, TaskStatus

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
    opportunity_id = Column(Integer, ForeignKey("opportunity.id"))

    owner = relationship("User", foreign_keys=[owner_id])
    opportunity = relationship("Opportunity", back_populates="tasks")

    @property
    def parent(self):
        """Returns the opportunity of the task"""
        return self.opportunity


# Pydantic models
class OpportunityRead(AppBase):
    id: int
    name: str


class TaskBase(AppBase):
    description: str
    due_date: date
    owner_id: int
    priority: Priority | None = Priority.medium


class TaskCreate(TaskBase):
    status: TaskStatus = TaskStatus.not_started
    opportunity_id: int


class TaskRead(UserTimeStampBase, TaskBase):
    id: int
    completed_on: datetime | None = None
    is_required: bool
    status: TaskStatus
    owner: UserSummary
    opportunity: OpportunityRead


class TaskUpdate(TaskBase):
    description: str | None = None
    due_date: date | None = None
    owner_id: int | None = None
    status: TaskStatus | None = None
