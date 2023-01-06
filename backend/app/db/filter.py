from collections import namedtuple
from collections.abc import Iterable
from six import string_types
from itertools import chain
from sqlalchemy import and_, not_, or_, func
from sqlalchemy.sql.expression import Select

from app.core.exceptions import BadFilterFormat
from app.db.utilities import auto_join, get_model_from_spec, get_sqlalchemy_field


BooleanFunction = namedtuple("BooleanFunction", ("key", "sqlalchemy_fn", "only_one_arg"))
BOOLEAN_FUNCTIONS = [
    BooleanFunction("or", or_, False),
    BooleanFunction("and", and_, False),
    BooleanFunction("not", not_, True),
]


class Operator:

    OPERATORS = {
        "==": lambda f, v: f == v,
        "equals": lambda f, v: f == v,
        "!=": lambda f, v: f != v,
        "notEquals": lambda f, v: f != v,
        ">": lambda f, v: f > v,
        "gt": lambda f, v: f > v,
        "<": lambda f, v: f < v,
        "lt": lambda f, v: f < v,
        ">=": lambda f, v: f >= v,
        "gte": lambda f, v: f >= v,
        "<=": lambda f, v: f <= v,
        "lte": lambda f, v: f <= v,
        "startsWith": lambda f, v: func.lower(f).startswith(v.lower()),
        "endsWith": lambda f, v: func.lower(f).endswith(v.lower()),
        "contains": lambda f, v: func.lower(f).contains(v.lower()),
        "notContains": lambda f, v: ~func.lower(f).contains(v.lower()),
        "in": lambda f, v: f.in_(v),
        "not_in": lambda f, v: ~f.in_(v),
        "dateIs": lambda f, v: f == v,
        "dateIsNot": lambda f, v: f != v,
        "dateBefore": lambda f, v: f < v,
        "dateAfter": lambda f, v: f > v,
        "between": lambda f, v: f.between(v[0], v[1]),
    }

    def __init__(self, operator: str | None = None):
        if not operator:
            operator = "=="

        if operator not in self.OPERATORS:
            raise BadFilterFormat(f"Operator {operator} not valid.")

        self.operator = operator
        self.function = self.OPERATORS[operator]


class Filter:
    def __init__(self, filter_spec: dict):
        self.filter_spec = filter_spec

        try:
            filter_spec["field"]
        except KeyError:
            raise BadFilterFormat("'field' is a mandatory filter attribute")
        except TypeError:
            raise BadFilterFormat(f"Filter spec {filter_spec} should be a dictionary")

        self.operator = Operator(filter_spec.get("operator"))
        if "value" in filter_spec:
            self.value = filter_spec.get("value")
        else:
            raise BadFilterFormat("'value' must be provided")

    def get_named_models(self):
        if "model" in self.filter_spec:
            return {self.filter_spec["model"]}
        return set()

    def format_for_sqlalchemy(self, default_model):
        value = self.value
        function = self.operator.function
        field_name = self.filter_spec["field"]

        model = get_model_from_spec(self.filter_spec, default_model)
        field = get_sqlalchemy_field(model, field_name)
        return function(field, value)


class BooleanFilter:
    def __init__(self, function, *filters) -> None:
        self.function = function
        self.filters = filters

    def get_named_models(self):
        models = set()
        for filter in self.filters:
            models.update(filter.get_named_models())
        return models

    def format_for_sqlalchemy(self, default_model):
        return self.function(
            *[filter.format_for_sqlalchemy(default_model=default_model) for filter in self.filters]
        )


def _is_iterable_filter(filter_spec):
    """`filter_spec` may be a list of nested filter specs, or a dict."""
    return isinstance(filter_spec, Iterable) and not isinstance(filter_spec, (string_types, dict))


def build_filters(filter_spec):
    """Recursively process `filter_spec`"""
    if _is_iterable_filter(filter_spec):
        return list(chain.from_iterable(build_filters(item) for item in filter_spec))

    if isinstance(filter_spec, dict):
        for boolean_function in BOOLEAN_FUNCTIONS:
            if boolean_function.key in filter_spec:
                # The filter spec is for a boolean function
                # Get the function argument definitions and validate
                fn_args = filter_spec[boolean_function.key]

                if not _is_iterable_filter(fn_args):
                    raise BadFilterFormat(
                        f"{boolean_function.key} value must be an iterable across the function"
                    )

                return [BooleanFilter(boolean_function.sqlalchemy_fn, *build_filters(fn_args))]

    return [Filter(filter_spec=filter_spec)]


def get_named_models(filters):
    models = set()
    for filter in filters:
        models.update(filter.get_named_models())
    return models


def apply_filters(query: Select, default_model, filter_spec: list[dict] | dict):
    filters = build_filters(filter_spec=filter_spec)
    filter_models = get_named_models(filters=filters)
    query = auto_join(query, filter_models)

    sqlalchemy_filters = [
        filter.format_for_sqlalchemy(default_model=default_model) for filter in filters
    ]

    if sqlalchemy_filters:
        query = query.where(*sqlalchemy_filters)

    return query
