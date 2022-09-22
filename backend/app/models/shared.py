from sqlalchemy import Integer, Column, String

from app.db.base import Base

# SQLAlchemy models
class Tenant(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, index=True, unique=True)
    schema = Column(String, nullable=False, unique=True)
    host = Column(String, nullable=False, unique=True)

    __table_args__ = {"schema": "shared"}


class Language(Base):
    code = Column(String(2), primary_key=True)

    __table_args__ = {"schema": "shared"}


class Country(Base):
    code = Column(String(2), primary_key=True)

    __table_args__ = {"schema": "shared"}


class Currency(Base):
    code = Column(String(3), primary_key=True)

    __table_args__ = {"schema": "shared"}
