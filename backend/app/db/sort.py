from sqlalchemy.sql.expression import Select

from app.core.exceptions import BadSortFormat
from app.db.utilities import auto_join, get_model_from_spec, get_sqlalchemy_field

SORT_ASCENDING = 1
SORT_DESCENDING = -1


class Sort:
    def __init__(self, sort_spec: dict):
        self.sort_spec = sort_spec

        try:
            field_name = sort_spec["field"]
            order = sort_spec["order"]
        except KeyError:
            raise BadSortFormat("'field' and 'order' are mandatory attributes")
        except TypeError:
            raise BadSortFormat(f"Sort spec {sort_spec} should be a dictionary")

        if order not in [SORT_ASCENDING, SORT_DESCENDING]:
            raise BadSortFormat(f"Order {order} not valid")

        self.field_name = field_name
        self.order = order

    def get_named_models(self):
        if "model" in self.sort_spec:
            return {self.sort_spec["model"]}
        return set()

    def format_for_sqlalchemy(self, default_model):
        sort_spec = self.sort_spec
        order = self.order
        field_name = self.field_name

        model = get_model_from_spec(sort_spec, default_model)
        field = get_sqlalchemy_field(model, field_name)

        if order == SORT_ASCENDING:
            sort_fnc = field.asc
        elif order == SORT_DESCENDING:
            sort_fnc = field.desc

        return sort_fnc()


def get_named_models(sorts):
    models = set()
    for sort in sorts:
        models.update(sort.get_named_models())
    return models


def apply_sort(query: Select, default_model, sort_spec: list[dict] | dict):
    if isinstance(sort_spec, dict):
        sort_spec = [sort_spec]

    sorts = [Sort(item) for item in sort_spec]
    sort_models = get_named_models(sorts)
    query = auto_join(query, sort_models)

    sqlalchemy_sorts = [sort.format_for_sqlalchemy(default_model=default_model) for sort in sorts]

    if sqlalchemy_sorts:
        query = query.order_by(*sqlalchemy_sorts)

    return query
