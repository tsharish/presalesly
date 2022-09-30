from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud.answer import answer
from app.models.base import Page
from app.api.common import common_parameters
from app.models.user import User
from app.core.security import get_current_user
from app.models.answer import (
    AnswerCreate,
    AnswerRead,
    AnswerUpdate,
    AnswerRecommendation,
    Question,
)

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/", response_model=Page[AnswerRead], summary="Get all answer entries")
async def get_answers(common: dict = Depends(common_parameters)):
    return answer.get_all(**common)


@router.get("/{id}", response_model=AnswerRead, summary="Get an answer entry based on the ID")
async def get_answer(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    result = answer.get(db=db, id=id, user=user)
    if not result:
        raise HTTPException(status_code=404, detail="The answer entry with this ID does not exist.")
    return result


@router.post("/", response_model=AnswerRead, summary="Create an answer entry")
async def create_answer(
    answer_in: AnswerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return answer.create(db=db, obj_in=answer_in, user=user)


@router.put("/{id}", response_model=AnswerRead, summary="Update an existing answer entry")
async def update_answer(
    id: int,
    answer_in: AnswerUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    answer_to_update = answer.get(db=db, id=id, user=user)
    if not answer_to_update:
        raise HTTPException(status_code=404, detail="The answer entry with this ID does not exist.")
    return answer.update(db=db, db_obj=answer_to_update, obj_in=answer_in, user=user)


@router.delete("/{id}", summary="Delete an answer entry")
async def delete_answer(
    id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    answer_to_delete = answer.get(db=db, id=id, user=user)
    if not answer_to_delete:
        raise HTTPException(status_code=404, detail="The answer entry with this ID does not exist.")
    answer.delete(db=db, db_obj=answer_to_delete, user=user)
    return {"message": f"Answer entry {id} has been deleted successfully"}


@router.post(
    "/recommend",
    response_model=list[AnswerRecommendation],
    summary="Get answer recommendations based on the question",
)
async def recommend_answers(
    question: Question,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return answer.get_recommendations(question=question, db=db, user=user)
