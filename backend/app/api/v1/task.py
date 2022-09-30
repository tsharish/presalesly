from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.task import task
from app.models.base import Page
from app.api.common import common_parameters
from app.models.user import User
from app.core.security import get_current_user
from app.models.task import TaskCreate, TaskRead, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=Page[TaskRead], summary="Get all tasks for the current user")
async def get_tasks(common: dict = Depends(common_parameters)):
    return task.get_all(**common)


@router.get("/{id}", response_model=TaskRead, summary="Get a task based on the ID")
async def get_task(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    result = task.get(db=db, id=id, user=user)
    if not result:
        raise HTTPException(status_code=404, detail="The task with this ID does not exist.")
    return result


@router.get(
    "/opportunity/{id}",
    response_model=list[TaskRead],
    summary="Get all tasks based on the opportunity ID",
)
async def get_tasks_by_opp(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    result = task.get_by_opp(db=db, opp_id=id, user=user)
    if not result:
        raise HTTPException(status_code=404, detail="No tasks for this opportunity were found.")
    return result


@router.post("/", response_model=TaskRead, summary="Create a task")
async def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return task.create(db=db, obj_in=task_in, user=user)


@router.put("/{id}", response_model=TaskRead, summary="Update an existing task")
async def update_task(
    id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    task_to_update = task.get(db=db, id=id, user=user)
    if not task_to_update:
        raise HTTPException(status_code=404, detail="The task with this ID does not exist.")
    return task.update(db=db, db_obj=task_to_update, obj_in=task_in, user=user)


@router.delete("/{id}", summary="Delete a task")
async def delete_task(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    task_to_delete = task.get(db=db, id=id, user=user)
    if not task_to_delete:
        raise HTTPException(status_code=404, detail="The task with this ID does not exist.")
    task.delete(db=db, db_obj=task_to_delete, user=user)
    return {"message": f"Task {id} has been deleted successfully"}
