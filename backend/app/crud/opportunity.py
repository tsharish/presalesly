import math
import pandas as pd
from typing import Final
from datetime import timedelta, datetime
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
    ALLOWED_ROLES_ALL: Final = ["ADMIN"]

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
            opp_template_tasks: list[OppTemplateTask] = (
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
                        due_date=obj_in.start_date + timedelta(days=row.due_date_offset),  # type: ignore
                        owner_id=obj_in.owner_id,
                        priority=row.priority,
                        is_required=row.is_required,
                        status=TaskStatus.not_started,
                        opportunity_id=db_opp.id,
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
            db_obj.status = get_status_from_opp_stage(db=db, stage_id=obj_in.stage_id)  # type: ignore

        super().update(db, db_obj, obj_in, user)
        return self.update_opp_score(db=db, opportunity=db_obj)

    def update_opp_score(self, db: Session, opportunity: Opportunity):
        """Calculates & updates the opportunity AI Score in the database"""
        # This must be called after the underlying Create or Update has been committed
        opportunity.ai_score = opp_score.predict(opportunity_id=opportunity.id)  # type: ignore
        db.add(opportunity)
        db.commit()
        db.refresh(opportunity)
        return opportunity

    def get_user_dashboard(self, db: Session, user: User):
        """Returns opportunity dashboard data for the user"""
        opp_df = pd.read_sql_query(
            select(
                Opportunity.id,
                Opportunity.status,
                Opportunity.age,
                Opportunity.close_month.label("close_month"),
                Opportunity.close_quarter.label("close_quarter"),
                Opportunity.close_year.label("close_year"),
            ).where(Opportunity.owner_id == user.id),
            db.connection(),
        )

        (
            open_opportunities,
            won_opp_current_month,
            won_opp_current_quarter,
            average_time_to_close,
        ) = self._calc_dashboard_kpi(opp_df=opp_df)

        return {
            "open_opportunities": open_opportunities,
            "won_opp_current_month": won_opp_current_month,
            "won_opp_current_quarter": won_opp_current_quarter,
            "average_time_to_close": average_time_to_close,
        }

    def get_admin_dashboard(self, db: Session, user: User):
        """Returns dashboard data for all opportunities"""
        if user.role_id not in self.ALLOWED_ROLES_ALL:
            raise permission_exception

        opp_df = pd.read_sql_query(
            select(
                Opportunity.id,
                Opportunity.status,
                Opportunity.stage_id,
                Opportunity.expected_amount,
                Opportunity.age,
                Opportunity.close_month.label("close_month"),
                Opportunity.close_quarter.label("close_quarter"),
                Opportunity.close_year.label("close_year"),
            ),
            db.connection(),
        )

        (
            open_opportunities,
            won_opp_current_month,
            won_opp_current_quarter,
            average_time_to_close,
        ) = self._calc_dashboard_kpi(opp_df=opp_df)

        stages, expected_amount = self._calc_pipeline(opp_df=opp_df, db=db)

        return {
            "open_opportunities": open_opportunities,
            "won_opp_current_month": won_opp_current_month,
            "won_opp_current_quarter": won_opp_current_quarter,
            "average_time_to_close": average_time_to_close,
            "pipeline": {"stages": stages, "expected_amount": expected_amount},
        }

    def _calc_dashboard_kpi(self, opp_df: pd.DataFrame):
        current_month = datetime.now().month
        current_quarter = (current_month - 1) // 3 + 1
        current_year = datetime.now().year

        open_opp_df = opp_df[opp_df["status"] == OppStatus.open].copy()
        won_opp_df = opp_df[opp_df["status"] == OppStatus.won].copy()

        won_opp_current_month = len(
            won_opp_df[
                (won_opp_df["close_month"] == current_month)
                & (won_opp_df["close_year"] == current_year)
            ]
        )
        won_opp_current_quarter = len(
            won_opp_df[
                (won_opp_df["close_quarter"] == current_quarter)
                & (won_opp_df["close_year"] == current_year)
            ]
        )
        open_opportunities = len(open_opp_df)
        average_time_to_close = won_opp_df["age"].mean()

        if math.isnan(average_time_to_close):
            average_time_to_close = 0

        return (
            open_opportunities,
            won_opp_current_month,
            won_opp_current_quarter,
            average_time_to_close,
        )

    def _calc_pipeline(self, opp_df: pd.DataFrame, db: Session):
        open_opp_df = opp_df[opp_df["status"] == OppStatus.open].copy()
        open_opp_df_sum = open_opp_df.groupby("stage_id")["expected_amount"].sum()
        opp_stage_df = pd.read_sql_query(
            select(OppStage.id, OppStage.sort_order, OppStage.description.label("stage")),
            db.connection(),
        )
        pipeline_df = pd.merge(
            open_opp_df_sum, opp_stage_df, how="left", left_on="stage_id", right_on="id"
        )

        return pipeline_df["stage"].tolist(), pipeline_df["expected_amount"].tolist()


opportunity = CRUDOpp(Opportunity)


def get_status_from_opp_stage(db: Session, stage_id: int) -> str:
    """Gets the default status from the Opportunity Stage"""
    opp_stage = db.execute(select(OppStage).where(OppStage.id == stage_id)).scalars().one_or_none()
    return opp_stage.opp_status
