from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.base import AppBase
from app.models.user import UserTimeStampMixin, UserTimeStampBase
from app.core.enums import Priority

# SQLAlchemy models
class OppTemplate(Base, UserTimeStampMixin):
    __tablename__ = "opp_template"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    opp_template_tasks = relationship("OppTemplateTask")

    @classmethod
    def get_resource_type(cls):
        return "setting"


class OppTemplateTask(Base, UserTimeStampMixin):
    __tablename__ = "opp_template_task"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    opp_template_id = Column(Integer, ForeignKey("opp_template.id", ondelete="CASCADE"))
    due_date_offset = Column(Integer)
    priority = Column(String, default=Priority.medium)
    is_required = Column(Boolean, default=False)

    @classmethod
    def get_resource_type(cls):
        return "setting"


# Pydantic models
class OppTemplateTaskBase(AppBase):
    description: str
    due_date_offset: int
    priority: Priority | None = Priority.medium
    is_required: bool | None = False


class OppTemplateTaskCreate(OppTemplateTaskBase):
    opp_template_id: int


class OppTemplateTaskRead(UserTimeStampBase, OppTemplateTaskBase):
    id: int
    opp_template_id: int


class OppTemplateTaskUpdate(OppTemplateTaskBase):
    description: str | None = None
    due_date_offset: int | None = None


class OppTemplateBase(AppBase):
    description: str
    is_active: bool | None = True


class OppTemplateCreate(OppTemplateBase):
    ...


class OppTemplateRead(UserTimeStampBase, OppTemplateBase):
    id: int
    opp_template_tasks: list[OppTemplateTaskRead] | None = None


class OppTemplateUpdate(OppTemplateBase):
    description: str | None = None
