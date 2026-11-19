from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.analyses import router as analyses_router
from app.api.products import router as products_router
from app.config import CATALOG_DIR, RESULT_DIR
from app.database import Base, engine
from app import models  # noqa: F401 - registers ORM models


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="AI Retail Shelf Analyzer", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/results", StaticFiles(directory=RESULT_DIR), name="results")
app.mount("/catalog-images", StaticFiles(directory=CATALOG_DIR), name="catalog-images")
app.include_router(analyses_router)
app.include_router(products_router)


@app.get("/health")
def health():
    return {"status": "ok"}
