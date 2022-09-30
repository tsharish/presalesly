from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.opp_template import opp_template, opp_template_task
from app.models.base import Page
from app.api.common import common_parameters
from app.models.user import User
from app.core.security import get_current_user
from app.models.opp_template import (
    OppTemplateCreate,
    OppTemplateRead,
    OppTemplateUpdate,
    OppTemplateTaskCreate,
    OppTemplateTaskRead,
    OppTemplateTaskUpdate,
)

opp_template_router = APIRouter(prefix="/opp_templates", tags=["opportunity templates"])
opp_template_task_router = APIRouter(
    prefix="/opp_template_tasks", tags=["opportunity template tasks"]
)


@opp_template_router.get(
    "/", response_model=Page[OppTemplateRead], summary="Get all opportunity templates"
)
async def get_opp_templates(common: dict = Depends(common_parameters)):
    return opp_template.get_all(**common)


@opp_template_router.get(
    "/{id}",
    response_model=OppTemplateRead,
    summary="Get an opportunity template based on the ID",
)
async def get_opp_template(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    result = opp_template.get(db=db, id=id, user=user)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="The opportunity template with this ID does not exist.",
        )
    return result


@opp_template_router.post(
    "/", response_model=OppTemplateRead, summary="Create an opportunity template"
)
async def create_opp_template(
    opp_template_in: OppTemplateCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return opp_template.create(db=db, obj_in=opp_template_in, user=user)


@opp_template_router.put(
    "/{id}",
    response_model=OppTemplateRead,
    summary="Update an existing opportunity template",
)
async def update_opp_template(
    id: int,
    opp_template_in: OppTemplateUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    opp_template_to_update = opp_template.get(db=db, id=id, user=user)
    if not opp_template_to_update:
        raise HTTPException(
            status_code=404,
            detail="The opportunity template with this ID does not exist.",
        )
    return opp_template.update(
        db=db, db_obj=opp_template_to_update, obj_in=opp_template_in, user=user
    )


@opp_template_router.delete("/{id}", summary="Delete an opportunity template")
async def delete_opp_template(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    opp_template_to_delete = opp_template.get(db=db, id=id, user=user)
    if not opp_template_to_delete:
        raise HTTPException(
            status_code=404,
            detail="The opportunity template with this ID does not exist.",
        )
    opp_template.delete(db=db, db_obj=opp_template_to_delete, user=user)
    return {"message": f"Opportunity template {id} has been deleted successfully"}


@opp_template_task_router.get(
    "/opp_template/{id}",
    response_model=list[OppTemplateTaskRead],
    summary="Get all tasks based on opportunity template ID",
)
async def get_tasks_by_opp_template(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    result = opp_template_task.get_by_opp_template(db=db, opp_template_id=id, user=user)
    if not result:
        raise HTTPException(
            status_code=404, detail="No tasks for this opportunity template were found."
        )
    return result


@opp_template_task_router.post(
    "/",
    response_model=OppTemplateTaskRead,
    summary="Add a task to an opportunity template",
)
async def create_opp_template_task(
    opp_template_task_in: OppTemplateTaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return opp_template_task.create(db=db, obj_in=opp_template_task_in, user=user)


@opp_template_task_router.put(
    "/{id}",
    response_model=OppTemplateTaskRead,
    summary="Update a task in an opportunity template",
)
async def update_opp_template_task(
    id: int,
    opp_template_task_in: OppTemplateTaskUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    opp_template_task_to_update = opp_template_task.get(db=db, id=id, user=user)
    if not opp_template_task_to_update:
        raise HTTPException(
            status_code=404,
            detail="The opportunity template task with this ID does not exist.",
        )
    return opp_template_task.update(
        db=db,
        db_obj=opp_template_task_to_update,
        obj_in=opp_template_task_in,
        user=user,
    )


@opp_template_task_router.delete("/{id}", summary="Delete a task in an opportunity template")
async def delete_opp_template_task(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    opp_template_task_to_delete = opp_template_task.get(db=db, id=id, user=user)
    if not opp_template_task_to_delete:
        raise HTTPException(
            status_code=404,
            detail="The opportunity template task with this ID does not exist.",
        )
    opp_template_task.delete(db=db, db_obj=opp_template_task_to_delete, user=user)
    return {"message": f"Opportunity template task {id} has been deleted successfully"}
