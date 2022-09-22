from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.core.permissions import permission_exception
from app.models.opp_template import (
    OppTemplate,
    OppTemplateCreate,
    OppTemplateUpdate,
    OppTemplateTask,
    OppTemplateTaskCreate,
    OppTemplateTaskUpdate,
)


class CRUDOppTemplateTask(CRUDBase[OppTemplateTask, OppTemplateTaskCreate, OppTemplateTaskUpdate]):
    def get_by_opp_template(
        self, db: Session, opp_template_id: int, user: User
    ) -> list[OppTemplateTask] | None:
        if user.role_id == "ADMIN":
            return (
                db.execute(
                    select(OppTemplateTask).where(
                        OppTemplateTask.opp_template_id == opp_template_id
                    )
                )
                .scalars()
                .all()
            )
        else:
            raise permission_exception


opp_template = CRUDBase[OppTemplate, OppTemplateCreate, OppTemplateUpdate](OppTemplate)
opp_template_task = CRUDOppTemplateTask(OppTemplateTask)
