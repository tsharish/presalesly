from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.base import CRUDBaseDesc
from app.models.base import Page
from app.api.common import common_parameters
from app.models.user import User
from app.core.security import get_current_user
from app.models.industry import (
    Industry,
    IndustryDescription,
    IndustryCreate,
    IndustryRead,
    IndustryUpdate,
)

router = APIRouter(prefix="/industries", tags=["industries"])
industry = CRUDBaseDesc[Industry, IndustryDescription, IndustryCreate, IndustryUpdate](
    Industry, IndustryDescription
)


@router.get("/", response_model=Page[IndustryRead], summary="Get all industries")
async def get_industries(common: dict = Depends(common_parameters)):
    return industry.get_all(**common)


@router.get("/{id}", response_model=IndustryRead, summary="Get an industry based on the ID")
async def get_industry(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    result = industry.get(db=db, id=id, user=user)
    if not result:
        raise HTTPException(status_code=404, detail="The industry with this ID does not exist.")
    return result


@router.post("/", response_model=IndustryRead, summary="Create an industry")
async def create_industry(
    industry_in: IndustryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return industry.create(db=db, obj_in=industry_in, user=user)


@router.put("/{id}", response_model=IndustryRead, summary="Update an existing industry")
async def update_industry(
    id: int,
    industry_in: IndustryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    industry_to_update = industry.get(db=db, id=id, user=user)
    if not industry_to_update:
        raise HTTPException(status_code=404, detail="The industry with this ID does not exist.")
    return industry.update(db=db, db_obj=industry_to_update, obj_in=industry_in, user=user)


@router.delete("/{id}", summary="Delete an industry")
async def delete_industry(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    industry_to_delete = industry.get(db=db, id=id, user=user)
    if not industry_to_delete:
        raise HTTPException(status_code=404, detail="The industry with this ID does not exist.")
    industry.delete(db=db, db_obj=industry_to_delete, user=user)
    return {"message": f"Industry {id} has been deleted successfully"}
