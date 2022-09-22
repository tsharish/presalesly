from collections import namedtuple
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select


Pagination = namedtuple("Pagination", ["total", "page", "size"])


def apply_pagination(db: Session, query: Select, offset: int, limit: int):
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    query = query.limit(limit).offset(offset)
    page = (offset / limit) + 1
    size = limit
    return query, Pagination(total, page, size)
