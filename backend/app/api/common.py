from contextvars import ContextVar
from fastapi import Depends, Query
from pydantic import Json
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import get_current_user
from app.db.session import get_db
from app.core.config import settings

language_code: ContextVar[str] = ContextVar("language_code", default=settings.DEFAULT_LANG_CODE)


async def common_parameters(
    db: Session = Depends(get_db),
    filter_spec: Json = Query([], alias="filter"),
    sort_spec: Json = Query([], alias="sort"),
    page: int = Query(default=1, ge=1, description="Page number"),
    size: int = Query(default=50, ge=1, le=100, description="Page size"),
    lang_code: str | None = None,
    user: User = Depends(get_current_user),
):
    if lang_code is not None:
        language_code.set(lang_code)
    return {
        "db": db,
        "filter_spec": filter_spec,
        "sort_spec": sort_spec,
        "offset": size * (page - 1),
        "limit": size,
        "user": user,
    }
