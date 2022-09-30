import shutil
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from pathlib import Path

from app.db.session import get_db, get_schema_from_request, db_schema
from app.crud.opportunity import opportunity
from app.models.base import Page
from app.api.common import common_parameters
from app.models.user import User
from app.core.security import get_current_user
from app.core.permissions import permission_exception
from app.models.opportunity import OpportunityCreate, OpportunityRead, OpportunityUpdate


router = APIRouter(prefix="/opportunities", tags=["opportunities"])


@router.get("/", response_model=Page[OpportunityRead], summary="Get all opportunities")
async def get_opportunities(common: dict = Depends(common_parameters)):
    return opportunity.get_all(**common)


@router.get("/open", response_model=Page[OpportunityRead], summary="Get all open opportunities")
async def get_open_opportunities(common: dict = Depends(common_parameters)):
    return opportunity.get_open(**common)


@router.get(
    "/{id}",
    response_model=OpportunityRead,
    summary="Get an opportunity based on the ID",
)
async def get_opportunity(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    result = opportunity.get(db=db, id=id, user=user)
    if not result:
        raise HTTPException(status_code=404, detail="The opportunity with this ID does not exist.")
    return result


@router.post("/", response_model=OpportunityRead, summary="Create an opportunity")
async def create_opportunity(
    opportunity_in: OpportunityCreate,
    db: Session = Depends(get_db),
    schema: str = Depends(get_schema_from_request),
    user: User = Depends(get_current_user),
):
    db_schema.set(schema)
    return opportunity.create(db=db, obj_in=opportunity_in, user=user)


@router.put("/{id}", response_model=OpportunityRead, summary="Update an existing opportunity")
async def update_opportunity(
    id: int,
    opportunity_in: OpportunityUpdate,
    db: Session = Depends(get_db),
    schema: str = Depends(get_schema_from_request),
    user: User = Depends(get_current_user),
):
    db_schema.set(schema)
    opportunity_to_update = opportunity.get(db=db, id=id, user=user)
    if not opportunity_to_update:
        raise HTTPException(status_code=404, detail="The opportunity with this ID does not exist.")
    return opportunity.update(db=db, db_obj=opportunity_to_update, obj_in=opportunity_in, user=user)


@router.delete("/{id}", summary="Delete an opportunity")
async def delete_opportunity(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    opportunity_to_delete = opportunity.get(db=db, id=id, user=user)
    if not opportunity_to_delete:
        raise HTTPException(status_code=404, detail="The opportunity with this ID does not exist.")
    opportunity.delete(db=db, db_obj=opportunity_to_delete, user=user)
    return {"message": f"Opportunity {id} has been deleted successfully"}


@router.post("/upload", summary="Upload a file containing opportunity data")
async def upload_opportunities(
    upload_file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    schema: str = Depends(get_schema_from_request),
):
    db_schema.set(schema)
    if user.role_id != "ADMIN":
        raise permission_exception
    destination = Path.cwd() / "upload"
    destination.mkdir(parents=True, exist_ok=True)

    filename = "opportunities_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
    destination = destination / filename
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
    opportunity.bulk_create(user=user, filepath=destination)
    return {"message": "Opportunities have been uploaded successfully"}


@router.put(
    "/{id}/update_opp_score",
    response_model=OpportunityRead,
    summary="Update the AI score for an opportunity",
)
async def update_opp_score(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    schema: str = Depends(get_schema_from_request),
):
    db_schema.set(schema)
    opportunity_to_update = opportunity.get(db=db, id=id, user=user)
    if not opportunity_to_update:
        raise HTTPException(status_code=404, detail="The opportunity with this ID does not exist.")
    return opportunity.update_opp_score(db=db, opportunity=opportunity_to_update)
