from sqlalchemy.sql.expression import Select
from sqlalchemy.exc import InvalidRequestError
import types

from app.db.base import get_class_by_tablename


def get_model_from_spec(spec, default_model):
    model_name = spec.get("model")
    if model_name is not None:
        # get model from model_name
        model = get_class_by_tablename(model_name)
    else:
        # use the default model
        model = default_model

    return model


def get_sqlalchemy_field(model, field_name: str):
    sqlalchemy_field = getattr(model, field_name)

    # If it's a hybrid method, then we call it so that we can work with
    # the result of the execution and not with the method object itself
    if isinstance(sqlalchemy_field, types.MethodType):
        sqlalchemy_field = sqlalchemy_field()

    return sqlalchemy_field


def auto_join(query: Select, models):
    for model_name in models:
        model = get_class_by_tablename(model_name)
        try:
            query = query.join(model)
        except InvalidRequestError:
            pass

    return query
