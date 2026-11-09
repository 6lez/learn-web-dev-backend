"""Точка входа FastAPI-приложения салона.

Запуск::

    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Документация: http://localhost:8000/docs
"""

from __future__ import annotations

from fastapi import FastAPI

from app.errors import register_error_handlers
from app.routers import categories

app = FastAPI(
    title="Салон красоты API",
    description="Учебное API: категории услуг, услуги и записи клиентов.",
    version="0.2.0",
)

register_error_handlers(app)
app.include_router(categories.router)


@app.get("/health", tags=["service"], summary="Проверка живости")
def health() -> dict[str, str]:
    return {"status": "ok"}
