from typing import Any, Generic, Type, TypeVar
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select
from pathlib import Path

from app.db.base import Base
from app.db.filter import apply_filters
from app.db.sort import apply_sort
from app.db.paginate import apply_pagination
from app.db.session import db_session, engine, db_schema
from app.core.permissions import permission_exception, has_permission
from app.core.enums import Permission
from app.models.user import User

# SQLAlchemy model type for the main object. Ex: "OppStage"
Model = TypeVar("Model", bound=Base)

# SQLAlchemy model type for the descriptions object. Ex: "OppStageDescription"
ModelDescription = TypeVar("ModelDescription", bound=Base)

# Pydantic model type for Create. Ex: "OppStageCreate"
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)

# Pydantic model type for Update. Ex: "OppStageUpdate"
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)

# Base CRUD class with default methods for Create, Read, Update, Delete (CRUD) operations
class CRUDBase(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[Model]) -> None:
        self.model = model

    def get(self, db: Session, id: Any, user: User) -> Model | None:
        """Returns the record based on the ID"""
        db_session.set(db)

        result = db.execute(select(self.model).where(self.model.id == id)).scalars().one_or_none()
        if result is not None:
            if not has_permission(user=user, resource=result, permission=Permission.read):
                raise permission_exception

        return result

    def get_all(
        self,
        db: Session,
        filter_spec: list[dict] | dict,
        sort_spec: list[dict] | dict,
        offset: int,
        limit: int,
        user: User,
        query: Select | None = None,
    ):
        """Returns all records"""
        if query is None:
            query = select(self.model)

        if filter_spec:
            query = apply_filters(query=query, default_model=self.model, filter_spec=filter_spec)

        if sort_spec:
            query = apply_sort(query=query, default_model=self.model, sort_spec=sort_spec)

        query, pagination = apply_pagination(db=db, query=query, offset=offset, limit=limit)

        if pagination.total == 0:
            raise HTTPException(status_code=404, detail="No records were found.")

        return {
            "items": db.execute(query).scalars().all(),
            "total": pagination.total,
            "page": pagination.page,
            "size": pagination.size,
        }

    def create(self, db: Session, obj_in: CreateSchema, user: User) -> Model:
        """Creates the record"""
        db_session.set(db)
        db_obj = self.model(**obj_in.dict(), created_by_id=user.id)

        if not has_permission(user=user, resource=db_obj, permission=Permission.create):
            raise permission_exception

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Model, obj_in: UpdateSchema, user: User) -> Model:
        """Updates the record"""
        db_session.set(db)

        if not has_permission(user=user, resource=db_obj, permission=Permission.update):
            raise permission_exception

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in update_data:
            if field in obj_data:
                setattr(db_obj, field, update_data[field])
        db_obj.updated_by_id = user.id

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Model, user: User) -> None:
        """Deletes the record"""
        db_session.set(db)

        if not has_permission(user=user, resource=db_obj, permission=Permission.delete):
            raise permission_exception

        db.delete(db_obj)
        db.commit()

    def bulk_create(self, user: User, filepath: Path) -> None:
        """Creates records in bulk using psycopg's COPY FROM functionality"""
        schema = db_schema.get()

        with filepath.open("r") as f:
            conn = engine.raw_connection()
            cursor = conn.cursor()

            if self.model.__name__ == "Account":
                cmd = f"""COPY {schema}.account (external_id, source_url, name, annual_revenue, 
                annual_revenue_curr_code, number_of_employees, street, address_line_2, 
                address_line_3, city, state, country_code, postal_code, fax, email, 
                phone, website, industry_id, is_active, created_by_id) 
                FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"""

            if self.model.__name__ == "Opportunity":
                cmd = f"""COPY {schema}.opportunity (external_id, name, account_id, 
                expected_amount, expected_amount_curr_code, start_date, close_date, 
                owner_id, probability, stage_id, status, created_by_id) 
                FROM STDIN WITH (FORMAT CSV, HEADER TRUE)"""

            cursor.copy_expert(cmd, f)
            conn.commit()


# Extends the Create and Update methods in the Base CRUD class for objects with associated descriptions object
class CRUDBaseDesc(
    CRUDBase[Model, CreateSchema, UpdateSchema],
    Generic[Model, ModelDescription, CreateSchema, UpdateSchema],
):
    def __init__(self, model: Type[Model], model_description: Type[ModelDescription]) -> None:
        self.model = model
        self.model_description = model_description

    def create(self, db: Session, obj_in: CreateSchema, user: User) -> Model:
        """Creates the record and the associated descriptions"""
        db_session.set(db)
        db_obj = self.model(**obj_in.dict(exclude={"descriptions"}), created_by_id=user.id)
        descriptions = obj_in.dict()["descriptions"]

        if not has_permission(user=user, resource=db_obj, permission=Permission.create):
            raise permission_exception

        for description in descriptions:
            db_obj_description = self.model_description(**description)
            db_obj.descriptions.append(db_obj_description)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Model, obj_in: UpdateSchema, user: User) -> Model:
        """Updates the record and the associated descriptions"""
        db_session.set(db)

        if not has_permission(user=user, resource=db_obj, permission=Permission.update):
            raise permission_exception

        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in update_data:
            if field in obj_data:
                setattr(db_obj, field, update_data[field])
        db_obj.updated_by_id = user.id

        if "descriptions" in update_data:
            # There are descriptions to be updated
            for item in update_data["descriptions"]:
                db_obj_desc = (
                    db.execute(
                        select(self.model_description).where(
                            and_(
                                self.model_description.id == db_obj.id,
                                self.model_description.language_code == item["language_code"],
                            )
                        )
                    )
                    .scalars()
                    .first()
                )

                if db_obj_desc:
                    # A description for that language already exists and must be updated
                    db_obj_desc.description = item["description"]
                    db.add(db_obj_desc)
                else:
                    # The description in this language does not exist and must be appended
                    db_obj_desc = self.model_description(**item)
                    db_obj.descriptions.append(db_obj_desc)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
