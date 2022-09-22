from datetime import timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import db_session
from app.crud.base import CRUDBase
from app.models.user import User
from app.core.permissions import has_permission, permission_exception
from app.core.enums import Permission, OppStatus, TaskStatus
from app.models.opp_template import OppTemplateTask
from app.models.opp_stage import OppStage
from app.models.task import Task
from app.models.opportunity import Opportunity, OpportunityCreate, OpportunityUpdate
from app.ml.opp_score import opp_score


class CRUDOpp(CRUDBase[Opportunity, OpportunityCreate, OpportunityUpdate]):
    ALLOWED_ROLES_ALL = ["ADMIN", "SUPER"]

    def get_all(
        self,
        db: Session,
        filter_spec: list[dict],
        sort_spec: list[dict],
        offset: int,
        limit: int,
        user: User,
    ):
        query = select(self.model)
        if user.role_id not in self.ALLOWED_ROLES_ALL:
            query = query.where(Opportunity.owner_id == user.id)
        return super().get_all(db, filter_spec, sort_spec, offset, limit, user, query)

    def get_open(
        self,
        db: Session,
        filter_spec: list[dict],
        sort_spec: list[dict],
        offset: int,
        limit: int,
        user: User,
    ):
        """Returns all open opportunities based on the role"""
        query = select(self.model).where(Opportunity.status == OppStatus.open)
        if user.role_id not in self.ALLOWED_ROLES_ALL:
            query = query.where(Opportunity.owner_id == user.id)
        return super().get_all(db, filter_spec, sort_spec, offset, limit, user, query)

    def create(self, db: Session, obj_in: OpportunityCreate, user: User) -> Opportunity:
        """Creates an opportunity"""
        db_session.set(db)
        status = get_status_from_opp_stage(db=db, stage_id=obj_in.stage_id)
        db_opp = Opportunity(**obj_in.dict(), status=status, created_by_id=user.id)

        if not has_permission(user=user, resource=db_opp, permission=Permission.create):
            raise permission_exception

        db.add(db_opp)

        # Flushing the Opportunity first so that we have the ID to record in the Task.
        # Flush instead of commit to ensure atomicity of the entire transaction
        # incl the tasks below.
        db.flush()

        # Add tasks to opportunity based on the opportunity template
        if obj_in.opp_template_id is not None:
            opp_template_tasks = (
                db.execute(
                    select(OppTemplateTask).where(
                        OppTemplateTask.opp_template_id == obj_in.opp_template_id
                    )
                )
                .scalars()
                .all()
            )

            if opp_template_tasks is not None:
                for row in opp_template_tasks:
                    db_task = Task(
                        description=row.description,
                        due_date=obj_in.start_date + timedelta(days=row.due_date_offset),
                        owner_id=obj_in.owner_id,
                        priority=row.priority,
                        is_required=row.is_required,
                        status=TaskStatus.not_started,
                        parent_type_id="opportunity",
                        parent_id=db_opp.id,
                        created_by_id=user.id,
                    )
                    db_opp.tasks.append(db_task)
                db.add(db_opp)

        db.commit()
        return self.update_opp_score(db=db, opportunity=db_opp)

    def update(
        self, db: Session, db_obj: Opportunity, obj_in: OpportunityUpdate, user: User
    ) -> Opportunity:
        """Updates an opportunity"""
        if obj_in.stage_id is not None:
            db_obj.status = get_status_from_opp_stage(db=db, stage_id=obj_in.stage_id)

        super().update(db, db_obj, obj_in, user)
        return self.update_opp_score(db=db, opportunity=db_obj)

    def update_opp_score(self, db: Session, opportunity: Opportunity):
        """Calculates & updates the opportunity AI Score in the database"""
        # This must be called after the underlying Create or Update has been committed
        opportunity.ai_score = opp_score.predict(opportunity_id=opportunity.id)
        db.add(opportunity)
        db.commit()
        db.refresh(opportunity)
        return opportunity


opportunity = CRUDOpp(Opportunity)


def get_status_from_opp_stage(db: Session, stage_id: int) -> str:
    """Gets the default status from the Opportunity Stage"""
    opp_stage = db.execute(select(OppStage).where(OppStage.id == stage_id)).scalars().one_or_none()
    return opp_stage.opp_status
