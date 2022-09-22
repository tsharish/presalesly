from fastapi import APIRouter, Depends

from app.api.v1.account import router as account_router
from app.api.v1.answer import router as answer_router
from app.api.v1.industry import router as industry_router
from app.api.v1.opp_score import router as opp_score_router
from app.api.v1.opp_stage import router as opp_stage_router
from app.api.v1.opp_template import opp_template_router, opp_template_task_router
from app.api.v1.opportunity import router as opportunity_router
from app.api.v1.task import router as task_router
from app.api.v1.users import auth_router
from app.api.v1.users import router as user_router
from app.core.security import get_current_user
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_URL)  # This is unauthenticated!
authenticated_api_router = APIRouter()

api_router.include_router(auth_router)

authenticated_api_router.include_router(user_router)
authenticated_api_router.include_router(opp_stage_router)
authenticated_api_router.include_router(industry_router)
authenticated_api_router.include_router(account_router)
authenticated_api_router.include_router(opportunity_router)
authenticated_api_router.include_router(task_router)
authenticated_api_router.include_router(opp_template_router)
authenticated_api_router.include_router(opp_template_task_router)
authenticated_api_router.include_router(answer_router)
authenticated_api_router.include_router(opp_score_router)

api_router.include_router(authenticated_api_router, dependencies=[Depends(get_current_user)])
