from typing import TypeVar, Generic
from pydantic import BaseModel
from pydantic.generics import GenericModel

ReadSchema = TypeVar("ReadSchema")


class AppBase(BaseModel):
    """Base Pydantic model for all other models"""

    class Config:
        orm_mode = True
        validate_assignment = True  # Performs validation on assignment
        arbitrary_types_allowed = True


class Page(GenericModel, Generic[ReadSchema]):
    """Base Generic Pydantic model for Pagination"""

    items: list[ReadSchema]
    total: int
    page: int
    size: int
