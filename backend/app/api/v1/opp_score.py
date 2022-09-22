from fastapi import APIRouter, Depends, HTTPException

from app.db.session import get_schema_from_request, db_schema
from app.models.user import User
from app.core.security import get_current_user
from app.core.permissions import permission_exception
from app.core.enums import MLAlgorithm, Scoring
from app.models.ml import ParamDist, Params, SearchResult, TrainResult
from app.ml.opp_score import opp_score

ALLOWED_ROLES = ["ADMIN"]
router = APIRouter(prefix="/opp_score", tags=["opportunity score"])


@router.post(
    "/search",
    response_model=SearchResult,
    summary="Search for opportunity score ML model with the best hyperparameters",
)
async def search_opp_score_model(
    param_dist: ParamDist,
    algorithm: MLAlgorithm = MLAlgorithm.lightgbm,
    scoring: Scoring = Scoring.f1,
    n_iterations: int = 50,
    set_best_as_default: bool = True,
    schema: str = Depends(get_schema_from_request),
    user: User = Depends(get_current_user),
):
    db_schema.set(schema)
    if user.role_id not in ALLOWED_ROLES:
        raise permission_exception
    results = opp_score.search(
        param_dist=param_dist,
        algorithm=algorithm,
        scoring=scoring,
        n_iterations=n_iterations,
        set_best_as_default=set_best_as_default,
    )
    if not results:
        raise HTTPException(status_code=404, detail="The operation yielded no results")
    return results


@router.post(
    "/train",
    response_model=TrainResult,
    summary="Train and evaluate opportunity score ML model",
)
async def train_opp_score_model(
    params: Params,
    algorithm: MLAlgorithm = MLAlgorithm.lightgbm,
    set_as_default: bool = True,
    schema: str = Depends(get_schema_from_request),
    user: User = Depends(get_current_user),
):
    db_schema.set(schema)
    if user.role_id not in ALLOWED_ROLES:
        raise permission_exception
    results = opp_score.train(algorithm=algorithm, params=params, set_as_default=set_as_default)
    if not results:
        raise HTTPException(status_code=404, detail="The operation yielded no results")
    return results
