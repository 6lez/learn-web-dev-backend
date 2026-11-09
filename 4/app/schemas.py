"""Pydantic-схемы: валидация входящих данных и формат ответов."""

from __future__ import annotations

from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

# Название и описание: непустая строка без ведущих/хвостовых пробелов, максимум 100 символов.
# min_length=1 отсекает "", strip_whitespace + проверка в валидаторе отсекает "   ".
NonEmptyText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]

MIN_DURATION = 30
MAX_DURATION = 180


class ServiceCreate(BaseModel):
    """Тело запроса POST /services.

    Ограничения:

    * ``title`` и ``desc`` — непустые строки до 100 символов;
    * ``duration`` — от 30 до 180 минут включительно;
    * ``price`` — строго больше 0;
    * ``categoryId`` — положительный идентификатор существующей категории
      (существование проверяется в роутере, т.к. нужен доступ к БД).
    """

    model_config = ConfigDict(extra="forbid")

    categoryId: int = Field(..., gt=0, examples=[3], description="Идентификатор категории")
    title: NonEmptyText = Field(..., examples=["Наращивание ресниц"])
    desc: NonEmptyText = Field(..., examples=["Огромные ресницы уже через 30 минут"])
    duration: int = Field(
        ...,
        ge=MIN_DURATION,
        le=MAX_DURATION,
        examples=[30],
        description="Продолжительность в минутах: 30..180",
    )
    price: Decimal = Field(..., gt=0, decimal_places=2, examples=[1500.00])


class ServiceOut(BaseModel):
    """Услуга в ответе API.

    В БД колонка называется ``category_id``, а в API — ``categoryId``,
    поэтому схема собирается функцией :func:`service_to_out`.
    """

    id: int
    categoryId: int
    title: str
    desc: str
    duration: int
    price: float  # в ответе отдаём обычное число, а не строку


def service_to_out(service) -> ServiceOut:
    """Преобразовать ORM-объект Service в схему ответа."""
    return ServiceOut(
        id=service.id,
        categoryId=service.category_id,
        title=service.title,
        desc=service.desc,
        duration=service.duration,
        price=float(service.price),
    )
