from datetime import datetime
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import get_class_by_tablename
from app.db.session import db_session
from app.crud.base import CRUDBase
from app.models.user import User
from app.core.permissions import has_permission, permission_exception
from app.core.enums import Permission, TaskStatus
from app.models.opportunity import Opportunity
from app.models.task import Task, TaskCreate, TaskUpdate


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def get_all(
        self,
        db: Session,
        filter_spec: list[dict],
        sort_spec: list[dict],
        offset: int,
        limit: int,
        user: User,
    ):
        """Returns all the tasks for the current user"""
        query = select(self.model).where(Task.owner_id == user.id)
        return super().get_all(db, filter_spec, sort_spec, offset, limit, user, query)

    def get_by_opp(self, db: Session, opp_id: int, user: User) -> list[Task] | None:
        """Returns all the tasks based on the Opportunity ID"""
        db_session.set(db)
        opportunity = (
            db.execute(select(Opportunity).where(Opportunity.id == opp_id)).scalars().one_or_none()
        )

        if not opportunity:
            raise HTTPException(
                status_code=404, detail="The opportunity with this ID does not exist"
            )

        # Check to ensure that the user has Read permission for the Opportunity
        if not has_permission(user=user, resource=opportunity, permission=Permission.read):
            raise permission_exception

        return (
            db.execute(
                select(Task).where(Task.parent_id == opp_id, Task.parent_type_id == "opportunity")
            )
            .scalars()
            .all()
        )

    def create(self, db: Session, obj_in: TaskCreate, user: User) -> Task:
        """Creates a task"""
        db_task = Task(**obj_in.dict(), created_by_id=user.id)

        # Get class from parent_type_id
        parent_model = get_class_by_tablename(obj_in.parent_type_id)

        # Get the parent object
        db_parent = (
            db.execute(select(parent_model).where(parent_model.id == obj_in.parent_id))
            .scalars()
            .one_or_none()
        )

        if not db_parent:
            raise HTTPException(status_code=404, detail="The parent object does not exist")

        # Add the task to the parent object and return the task
        db_parent.tasks.append(db_task)
        db.add(db_parent)
        db.commit()
        db.refresh(db_task)
        return db_task

    def update(self, db: Session, db_obj: Task, obj_in: TaskUpdate, user: User) -> Task:
        """Updates a task"""
        if obj_in.status == TaskStatus.completed:
            db_obj.completed_on = datetime.utcnow()
        return super().update(db, db_obj, obj_in, user)


task = CRUDTask(Task)
