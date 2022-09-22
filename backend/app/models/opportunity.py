from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, select, func
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.sql.expression import extract
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case
from datetime import date, timedelta
from pydantic import confloat, NonNegativeFloat, validator, root_validator

from app.core.constants import CURRENCIES
from app.db.base import Base
from app.models.base import AppBase
from app.models.user import UserSummary, UserTimeStampMixin, UserTimeStampBase
from app.core.enums import OppStatus, TaskStatus
from app.models.account import AccountSummary
from app.models.opp_stage import OppStageSummary
from app.models.task import Task, HasTasks

# SQLAlchemy models
class Opportunity(Base, HasTasks, UserTimeStampMixin):
    id = Column(Integer, primary_key=True)
    external_id = Column(String)
    name = Column(String, nullable=False)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)
    expected_amount = Column(Numeric(precision=15, scale=2), nullable=False)
    expected_amount_curr_code = Column(String, ForeignKey("shared.currency.code"), nullable=False)
    start_date = Column(Date, nullable=False)
    close_date = Column(Date, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"), index=True)
    probability = Column(Numeric(precision=5, scale=4))  # Valid interval is 0.0000 to 1.0000
    stage_id = Column(Integer, ForeignKey("opp_stage.id"))
    opp_template_id = Column(Integer, ForeignKey("opp_template.id"))
    status = Column(String, nullable=False, index=True)
    ai_score = Column(Integer)

    # Refer to https://docs.sqlalchemy.org/en/14/orm/mapped_sql_expr.html#using-column-property
    probability_percent = column_property(probability * 100)
    weighted_amount = column_property(probability * expected_amount)
    close_month = column_property(extract("MONTH", close_date))  # Month of the close date
    close_quarter = column_property(extract("QUARTER", close_date))  # Quarter of the close date
    close_year = column_property(extract("YEAR", close_date))  # Year of the close date
    not_started_task_count = column_property(
        select(func.count(Task.id))
        .where(
            Task.parent_id == id,
            Task.parent_type_id == "opportunity",
            Task.status == TaskStatus.not_started,
        )
        .correlate_except(Task)
        .scalar_subquery()
    )
    in_progress_task_count = column_property(
        select(func.count(Task.id))
        .where(
            Task.parent_id == id,
            Task.parent_type_id == "opportunity",
            Task.status == TaskStatus.in_progress,
        )
        .correlate_except(Task)
        .scalar_subquery()
    )
    completed_task_count = column_property(
        select(func.count(Task.id))
        .where(
            Task.parent_id == id,
            Task.parent_type_id == "opportunity",
            Task.status == TaskStatus.completed,
        )
        .correlate_except(Task)
        .scalar_subquery()
    )

    # Refer to https://docs.sqlalchemy.org/en/14/orm/mapped_sql_expr.html#using-a-hybrid
    @hybrid_property
    def age(self):
        if self.status == OppStatus.open:
            delta: timedelta = date.today() - self.start_date
            return delta.days
        else:
            delta: timedelta = self.close_date - self.start_date
            return delta.days

    @age.expression
    def age(cls):
        # Refer to https://stackoverflow.com/questions/42485952/calculate-datediff-in-postgres-using-sqlalchemy
        return case(
            [
                (
                    cls.status == OppStatus.open,
                    func.trunc(
                        (extract("EPOCH", func.current_date()) - extract("EPOCH", cls.start_date))
                        / 86400
                    ),
                ),
            ],
            else_=func.trunc(
                (extract("EPOCH", cls.close_date) - extract("EPOCH", cls.start_date)) / 86400
            ),
        )

    @hybrid_property
    def days_remaining(self):
        if self.status == OppStatus.open:
            delta: timedelta = self.close_date - date.today()
            return delta.days
        else:
            return 0

    @days_remaining.expression
    def days_remaining(cls):
        return case(
            [
                (
                    cls.status == OppStatus.open,
                    func.trunc(
                        (extract("EPOCH", cls.close_date) - extract("EPOCH", func.current_date()))
                        / 86400
                    ),
                ),
            ],
            else_=0,
        )

    account = relationship("Account", backref="opportunities")
    stage = relationship("OppStage")
    owner = relationship("User", foreign_keys=[owner_id], backref="opportunities")


# Pydantic models
class OpportunityBase(AppBase):
    external_id: str | None = None
    name: str
    expected_amount: NonNegativeFloat
    expected_amount_curr_code: str
    start_date: date
    close_date: date
    probability: confloat(ge=0, le=1)
    owner_id: int
    account_id: int
    stage_id: int

    @root_validator
    def check_close_after_start_date(cls, values):
        start_dt, close_dt = values.get("start_date"), values.get("close_date")
        if start_dt is not None and close_dt is not None:
            if start_dt > close_dt:
                raise ValueError("Start date must be before close date")
        return values

    @validator("expected_amount_curr_code")
    def validate_currency_code(cls, v):
        if v not in CURRENCIES:
            raise ValueError("Not a valid currency code")
        return v


class OpportunityCreate(OpportunityBase):
    opp_template_id: int | None = None


class OpportunityRead(UserTimeStampBase, OpportunityBase):
    id: int
    account: AccountSummary
    stage: OppStageSummary
    owner: UserSummary
    opp_template_id: int | None = None
    status: OppStatus
    ai_score: int | None = None
    probability_percent: float
    weighted_amount: float
    age: int
    days_remaining: int
    close_month: int
    close_quarter: int
    close_year: int
    not_started_task_count: int
    in_progress_task_count: int
    completed_task_count: int


class OpportunityUpdate(OpportunityBase):
    name: str | None = None
    account_id: int | None = None
    expected_amount: NonNegativeFloat | None = None
    expected_amount_curr_code: str | None = None
    start_date: date | None = None
    close_date: date | None = None
    owner_id: int | None = None
    probability: confloat(ge=0, le=1) | None = None
    stage_id: int | None = None
