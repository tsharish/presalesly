from typing import TypeVar, Generic
from pydantic import BaseModel
from pydantic.generics import GenericModel

ReadSchema = TypeVar("ReadSchema")

# Base Pydantic model for all other models to import from
class AppBase(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True  # Performs validation on assignment
        arbitrary_types_allowed = True


# Base Generic Pydantic model for Pagination
class Page(GenericModel, Generic[ReadSchema]):
    items: list[ReadSchema]
    total: int
    page: int
    size: int
