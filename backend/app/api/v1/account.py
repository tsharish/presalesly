import shutil
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from pathlib import Path

from app.db.session import get_db, get_schema_from_request, db_schema
from app.crud.base import CRUDBase
from app.models.base import Page
from app.api.common import common_parameters
from app.models.user import User
from app.core.security import get_current_user
from app.core.permissions import permission_exception
from app.models.account import Account, AccountCreate, AccountRead, AccountUpdate

router = APIRouter(prefix="/accounts", tags=["accounts"])
account = CRUDBase[Account, AccountCreate, AccountUpdate](Account)


@router.get("/", response_model=Page[AccountRead], summary="Get all accounts")
async def get_accounts(common: dict = Depends(common_parameters)):
    return account.get_all(**common)


@router.get("/{id}", response_model=AccountRead, summary="Get an account based on the ID")
async def get_account(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    result = account.get(db=db, id=id, user=user)
    if not result:
        raise HTTPException(status_code=404, detail="The account with this ID does not exist.")
    return result


@router.post("/", response_model=AccountRead, summary="Create an account")
async def create_account(
    account_in: AccountCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return account.create(db=db, obj_in=account_in, user=user)


@router.put("/{id}", response_model=AccountRead, summary="Update an existing account")
async def update_account(
    id: int,
    account_in: AccountUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    account_to_update = account.get(db=db, id=id, user=user)
    if not account_to_update:
        raise HTTPException(status_code=404, detail="The account with this ID does not exist.")
    return account.update(db=db, db_obj=account_to_update, obj_in=account_in, user=user)


@router.delete("/{id}", summary="Delete an account")
async def delete_account(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    account_to_delete = account.get(db=db, id=id, user=user)
    if not account_to_delete:
        raise HTTPException(status_code=404, detail="The account with this ID does not exist.")
    account.delete(db=db, db_obj=account_to_delete, user=user)
    return {"message": f"Account {id} has been deleted successfully"}


@router.post("/upload", summary="Upload a file containing account data")
async def upload_accounts(
    upload_file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    schema=Depends(get_schema_from_request),
):
    db_schema.set(schema)
    if user.role_id != "ADMIN":
        raise permission_exception
    destination = Path.cwd() / "upload"
    destination.mkdir(parents=True, exist_ok=True)

    filename = "accounts_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".csv"
    destination = destination / filename
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
    account.bulk_create(user=user, filepath=destination)
    return {"message": "Accounts have been uploaded successfully"}
