from app.models.base import AppBase


class Params(AppBase):
    n_estimators: int | None = None
    learning_rate: float | None = None
    max_depth: int | None = None
    reg_lambda: int | None = None  # l2 leaf regularization
    num_leaves: int | None = None  # Applicable more for LightGBM
    min_data_in_leaf: int | None = None


class ParamDist(AppBase):
    n_estimators_lower: int | None = None
    n_estimators_upper: int | None = None
    learning_rate_lower: float | None = None
    learning_rate_upper: float | None = None
    max_depth_lower: int | None = None
    max_depth_upper: int | None = None
    reg_lambda_lower: int | None = None
    reg_lambda_upper: int | None = None
    num_leaves_lower: int | None = None
    num_leaves_upper: int | None = None
    min_data_in_leaf_lower: int | None = None
    min_data_in_leaf_upper: int | None = None


class SearchResult(AppBase):
    best_score: float
    best_params: Params


class TrainResult(AppBase):
    accuracy: float
    f1: float
    precision: float
    recall: float
