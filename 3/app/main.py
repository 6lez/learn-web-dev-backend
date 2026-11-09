"""Точка входа FastAPI-приложения с БД.

Запуск::

    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

При первом запуске создаётся таблица ``masters`` и заполняется примерами.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, SessionLocal, engine
from app.models import Master
from app.routers import masters

SEED_MASTERS = [
    Master(name="Анна", specialization="Парикмахер"),
    Master(name="Мария", specialization="Визажист"),
    Master(name="Ольга", specialization="Мастер маникюра"),
    Master(name="Игорь", specialization="Парикмахер"),
]


def init_db() -> None:
    """Создать таблицы и заполнить ``masters`` примерами, если таблица пуста."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.query(Master).first() is None:
            db.add_all(SEED_MASTERS)
            db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Салон красоты API",
    description="Учебное API: мастера из базы данных.",
    version="0.3.0",
    lifespan=lifespan,
)

app.include_router(masters.router)


@app.get("/health", tags=["service"], summary="Проверка живости")
def health() -> dict[str, str]:
    return {"status": "ok"}
