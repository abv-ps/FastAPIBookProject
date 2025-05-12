from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import engine, get_db
from app.routers.author_router import router as author_router
from app.routers.book_router import router as book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await get_db()
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(
    title="Library API",
    description="API для управління авторами та книгами",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(author_router)
app.include_router(book_router)
