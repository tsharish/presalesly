from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.base import CRUDBaseDesc
from app.models.base import Page
from app.api.common import common_parameters
from app.models.user import User
from app.core.security import get_current_user
from app.models.opp_stage import (
    OppStage,
    OppStageDescription,
    OppStageCreate,
    OppStageRead,
    OppStageUpdate,
)

router = APIRouter(prefix="/opp_stage", tags=["opportunity stage"])
opp_stage = CRUDBaseDesc[OppStage, OppStageDescription, OppStageCreate, OppStageUpdate](
    OppStage, OppStageDescription
)


@router.get("/", response_model=Page[OppStageRead], summary="Get all opportunity stages")
async def get_opp_stages(common: dict = Depends(common_parameters)):
    return opp_stage.get_all(**common)


@router.get(
    "/{id}",
    response_model=OppStageRead,
    summary="Get an opportunity stage based on the ID",
)
async def get_opp_stage(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    result = opp_stage.get(db=db, id=id, user=user)
    if not result:
        raise HTTPException(
            status_code=404, detail="The opportunity stage with this ID does not exist."
        )
    return result


@router.post("/", response_model=OppStageRead, summary="Create an opportunity stage")
async def create_opp_stage(
    opp_stage_in: OppStageCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return opp_stage.create(db=db, obj_in=opp_stage_in, user=user)


@router.put("/{id}", response_model=OppStageRead, summary="Update an existing opportunity stage")
async def update_opp_stage(
    id: int,
    opp_stage_in: OppStageUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    opp_stage_to_update = opp_stage.get(db=db, id=id, user=user)
    if not opp_stage_to_update:
        raise HTTPException(
            status_code=404, detail="The opportunity stage with this ID does not exist."
        )
    return opp_stage.update(db=db, db_obj=opp_stage_to_update, obj_in=opp_stage_in, user=user)


@router.delete("/{id}", summary="Delete an opportunity stage")
async def delete_opp_stage(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    opp_stage_to_delete = opp_stage.get(db=db, id=id, user=user)
    if not opp_stage_to_delete:
        raise HTTPException(
            status_code=404, detail="The opportunity stage with this ID does not exist."
        )
    opp_stage.delete(db=db, db_obj=opp_stage_to_delete, user=user)
    return {"message": f"Opportunity stage {id} has been deleted successfully"}
