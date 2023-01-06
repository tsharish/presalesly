import logging
import time

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer

from app.api.v1 import api_router
from app.core.config import settings
from app.db.shared import init_database

logger = logging.getLogger(__name__)
handler = logging.FileHandler("file.log")
handler.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(format)
logger.addHandler(handler)

init_database()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http:\\/\\/.*localhost.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # Loading and saving the SBERT sentence embedding model on startup so that recommendations are faster
    # (https://shreyansh26.github.io/post/2020-11-30_fast_api_docker_ml_deploy/)
    embedder = SentenceTransformer(settings.SENT_EMB_MODEL)
    embedder.save(settings.SENT_EMB_MODEL_PATH)


# TODO: Need to enhance and test this
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.error(str(exc))
    return JSONResponse(
        status_code=500,
        content={"message": "An error occured. Please contact Presalesly for resolution."},
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Adds processing time to each header response"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router)


@app.get("/")
async def root(request: Request):
    return {
        "Host": request.headers["host"],
        "Host without port": request.headers["host"].split(":", 1)[0],
    }


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    # TODO: Add code to check database connection and other infrastructure statuses
    return {"health": "OK"}
