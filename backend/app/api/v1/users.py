from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.user import user
from app.models.base import Page
from app.api.common import common_parameters
from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.core.security import (
    get_current_user,
    authenticate_user,
    create_access_token,
    get_hashed_password,
    JWT_EXP,
)

router = APIRouter(prefix="/users", tags=["users"])
auth_router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/", response_model=Page[UserRead], summary="Get all users")
async def get_users(common: dict = Depends(common_parameters)):
    return user.get_all(**common)


@router.get("/{id}", response_model=UserRead, summary="Get a user based on the ID")
async def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = user.get(db=db, id=id, user=current_user)
    if not result:
        raise HTTPException(status_code=404, detail="The user with this ID does not exist.")
    return result


@router.post("/", response_model=UserRead, summary="Create a user")
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_in.password = get_hashed_password(user_in.password)
    return user.create(db=db, obj_in=user_in, user=current_user)


@router.put("/{id}", response_model=UserRead, summary="Update an existing user")
async def update_user(
    id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_to_update = user.get(db=db, id=id, user=current_user)
    if not user_to_update:
        raise HTTPException(status_code=404, detail="The user with this ID does not exist.")
    return user.update(db=db, db_obj=user_to_update, obj_in=user_in, user=current_user)


# TODO: The delete path function is for testing only and should be removed
@router.delete("/{id}", summary="Delete a user")
async def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_to_delete = user.get(db=db, id=id, user=current_user)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="The user with this ID does not exist.")
    user.delete(db=db, db_obj=user_to_delete, user=current_user)
    return {"message": f"User {id} has been deleted successfully"}


@auth_router.post("/login")
async def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db=db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=403, detail="User is not active")

    access_token_expires = timedelta(minutes=JWT_EXP)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
