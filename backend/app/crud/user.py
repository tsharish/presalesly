from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> User | None:
        """Returns a user based on the given email"""
        return db.execute(select(User).where(User.email == email)).scalars().one_or_none()


user = CRUDUser(User)
