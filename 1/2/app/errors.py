"""Ошибки приложения и их преобразование в HTTP-ответы.

FastAPI по умолчанию оборачивает ``HTTPException(detail="...")`` в JSON вида
``{"detail": "..."}``. В задании для 404 ожидается просто текст
``Category not found``, поэтому здесь заводятся собственные исключения и
глобальные обработчики: тело ответа — строка, а не объект.
"""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse


class AppError(Exception):
    """Базовое исключение приложения."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "Bad request"


class CategoryNotFoundError(AppError):
    """Категория с указанным id не найдена."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Category not found"


class ServiceNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Service not found"


class ValidationFailedError(AppError):
    """Данные не прошли валидацию."""

    status_code = 422
    message = "Validation error"


def _as_text_or_json(request: Request, exc: AppError):
    """Строкой отдаём только если клиент не ждёт JSON.

    Браузер и тесты curl получат человекочитаемый текст, а клиент с
    ``Accept: application/json`` — ``{"detail": "..."}``.
    """
    accept = request.headers.get("accept", "")
    if "application/json" in accept:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
    return PlainTextResponse(status_code=exc.status_code, content=exc.message)


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(CategoryNotFoundError, _as_text_or_json)
    app.add_exception_handler(ServiceNotFoundError, _as_text_or_json)
    app.add_exception_handler(ValidationFailedError, _as_text_or_json)
