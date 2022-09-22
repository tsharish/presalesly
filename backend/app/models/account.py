from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import EmailStr, AnyUrl, validator

from app.core.constants import COUNTRIES, CURRENCIES
from app.db.base import Base
from app.models.base import AppBase
from app.models.user import UserTimeStampMixin, UserTimeStampBase
from app.models.industry import IndustrySummary

# SQLAlchemy models
class Account(Base, UserTimeStampMixin):
    id = Column(Integer, primary_key=True)
    external_id = Column(String)
    source_url = Column(String)
    name = Column(String, nullable=False)
    annual_revenue = Column(Numeric(precision=15, scale=2))
    annual_revenue_curr_code = Column(String, ForeignKey("shared.currency.code"))
    number_of_employees = Column(Integer)
    street = Column(String)
    address_line_2 = Column(String)
    address_line_3 = Column(String)
    city = Column(String)
    state = Column(String)
    country_code = Column(String, ForeignKey("shared.country.code"), nullable=False)
    postal_code = Column(String)
    fax = Column(String)
    email = Column(String)
    phone = Column(String)
    website = Column(String)
    industry_id = Column(Integer, ForeignKey("industry.id"))
    is_active = Column(Boolean, default=True)

    industry = relationship("Industry")


# Pydantic models
class AccountBase(AppBase):
    external_id: str | None = None
    source_url: AnyUrl | None = None
    name: str
    annual_revenue: float | None = None
    annual_revenue_curr_code: str | None = None
    number_of_employees: int | None = None
    country_code: str
    street: str | None = None
    address_line_2: str | None = None
    address_line_3: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    fax: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    website: str | None = None
    is_active: bool | None = True

    @validator("annual_revenue_curr_code")
    def validate_currency_code(cls, v):
        if v is not None and v not in CURRENCIES:
            raise ValueError("Not a valid currency code")
        return v

    @validator("country_code")
    def validate_country_code(cls, v):
        if v not in COUNTRIES:
            raise ValueError("Not a valid country code")
        return v


class AccountCreate(AccountBase):
    industry_id: int | None = None


class AccountRead(UserTimeStampBase, AccountBase):
    id: int
    industry: IndustrySummary | None = None


class AccountUpdate(AccountBase):
    name: str | None = None
    country_code: str | None = None
    industry_id: int | None = None


class AccountSummary(AppBase):
    id: int
    name: str
