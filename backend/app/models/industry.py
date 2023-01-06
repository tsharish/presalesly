from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, select
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.db.base import Base
from app.models.base import AppBase
from app.models.user import UserTimeStampBase, UserTimeStampMixin
from app.api.common import language_code

# SQLAlchemy models
class IndustryDescription(Base, UserTimeStampMixin):
    __tablename__ = "industry_description"

    id = Column(Integer, ForeignKey("industry.id"), primary_key=True)
    language_code = Column(
        String, ForeignKey("shared.language.code"), primary_key=True, default="EN"
    )
    description = Column(String, nullable=False)


class Industry(Base, UserTimeStampMixin):
    id = Column(Integer, primary_key=True)
    external_id = Column(String)
    is_active = Column(Boolean, default=True)

    @hybrid_property
    def description(self):  # type: ignore
        """Sets the description from the descriptions table based on the language
        supplied in the route"""
        for item in self.descriptions:
            if item.language_code == language_code.get():
                return item.description

    @description.expression
    def description(cls):
        return (
            select(IndustryDescription.description)
            .where(
                IndustryDescription.id == cls.id,
                IndustryDescription.language_code == language_code.get(),
            )
            .scalar_subquery()
        )

    descriptions = relationship("IndustryDescription", cascade="all, delete-orphan")

    @classmethod
    def get_resource_type(cls):
        return "setting"


# Pydantic models
class Description(AppBase):
    language_code: str | None = "EN"
    description: str


class IndustryBase(AppBase):
    external_id: str | None = None
    is_active: bool | None = True
    descriptions: list[Description]


class IndustryCreate(IndustryBase):
    ...


class IndustryRead(UserTimeStampBase, IndustryBase):
    id: int
    description: str | None = None


class IndustryUpdate(IndustryBase):
    descriptions: list[Description] | None = None
