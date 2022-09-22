from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, select
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.ext.hybrid import hybrid_property
from pydantic import confloat

from app.db.base import Base
from app.models.base import AppBase
from app.models.user import UserTimeStampMixin, UserTimeStampBase
from app.core.enums import OppStatus
from app.api.common import language_code

# SQLAlchemy models
class OppStageDescription(Base, UserTimeStampMixin):
    __tablename__ = "opp_stage_description"

    id = Column(Integer, ForeignKey("opp_stage.id"), primary_key=True)
    language_code = Column(
        String, ForeignKey("shared.language.code"), primary_key=True, default="EN"
    )
    description = Column(String, nullable=False)


class OppStage(Base, UserTimeStampMixin):
    __tablename__ = "opp_stage"

    id = Column(Integer, primary_key=True)
    external_id = Column(String)
    default_probability = Column(Numeric(precision=5, scale=4), nullable=False)
    sort_order = Column(Integer, nullable=False, unique=True)
    opp_status = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    default_probability_percent = column_property(default_probability * 100)

    @hybrid_property
    def description(self):
        """Sets the description from the descriptions table
        based on the language supplied in the route"""
        for item in self.descriptions:
            if item.language_code == language_code.get():
                return item.description

    @description.expression
    def description(cls):
        return (
            select(OppStageDescription.description)
            .where(
                OppStageDescription.id == cls.id,
                OppStageDescription.language_code == language_code.get(),
            )
            .scalar_subquery()
        )

    descriptions = relationship(
        "OppStageDescription", backref="opp_stage", cascade="all, delete-orphan"
    )

    @classmethod
    def get_resource_type(cls):
        return "setting"


# Pydantic models
class Description(AppBase):
    language_code: str | None = "EN"
    description: str


class OppStageBase(AppBase):
    external_id: str | None = None
    default_probability: confloat(ge=0, le=1)  # Must be between 0 and 1
    sort_order: int
    opp_status: OppStatus
    is_active: bool | None = True
    descriptions: list[Description]


class OppStageCreate(OppStageBase):
    ...


class OppStageRead(UserTimeStampBase, OppStageBase):
    id: int
    description: str | None = None
    default_probability_percent: float


class OppStageUpdate(OppStageBase):
    default_probability: confloat(ge=0, le=1) | None = None
    sort_order: int | None = None
    opp_status: OppStatus | None = None
    descriptions: list[Description] | None = None


class OppStageSummary(AppBase):
    id: int
    description: str | None = None
