"""Точка входа FastAPI-приложения.

Запуск::

    uvicorn app.main:app --reload --host 0.0.0.0 --port 8003

При первом старте создаются таблицы ``categories`` и ``services``,
категории заполняются примерами.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, SessionLocal, engine
from app.models import Category
from app.routers import services

SEED_CATEGORIES = [
    Category(name="Стрижки и укладки"),
    Category(name="Маникюр и педикюр"),
    Category(name="Брови и ресницы"),
    Category(name="Спа-процедуры"),
]


def init_db() -> None:
    """Создать таблицы и заполнить категории, если их ещё нет."""
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.query(Category).first() is None:
            db.add_all(SEED_CATEGORIES)
            db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Салон красоты API",
    description="Учебное API: услуги в категориях.",
    version="0.4.0",
    lifespan=lifespan,
)

app.include_router(services.router)


@app.get("/health", tags=["service"], summary="Проверка живости")
def health() -> dict[str, str]:
    return {"status": "ok"}
