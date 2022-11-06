from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.base import AppBase
from app.models.user import UserTimeStampMixin, UserTimeStampBase, UserSummary
from app.models.task import HasTasks

# SQLAlchemy models
class Answer(Base, HasTasks, UserTimeStampMixin):
    id = Column(Integer, primary_key=True)
    language_code = Column(String, ForeignKey("shared.language.code"), default="EN")
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    is_active = Column(Boolean, default=True)

    owner = relationship("User", foreign_keys=[owner_id])


# Pydantic models
class AnswerBase(AppBase):
    language_code: str
    question: str
    answer: str
    owner_id: int
    is_active: bool


class AnswerCreate(AnswerBase):
    ...


class AnswerRead(UserTimeStampBase, AnswerBase):
    id: int
    owner: UserSummary


class AnswerUpdate(AnswerBase):
    language_code: str | None = None
    question: str | None = None
    answer: str | None = None
    owner_id: int | None = None
    is_active: bool | None = None


class Question(AppBase):
    query: str
    language_code: str | None = None


class AnswerRecommendation(AppBase):
    answer: AnswerRead
    score: int
