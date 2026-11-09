"""Задания 1 и 2: эндпоинты категорий услуг.

* ``GET /categories``               — все категории с количеством услуг;
* ``GET /categories/{category_id}`` — информация о конкретной категории.
"""

from __future__ import annotations

from fastapi import APIRouter, status

from app.errors import CategoryNotFoundError
from app.models import CategoryDetailOut, CategoryOut
from app.storage import count_services_in_category, get_category, list_categories

router = APIRouter(prefix="/categories", tags=["categories"])


def _to_out(category_id: int, name: str) -> CategoryOut:
    """Собрать ответ: категория + servicesCount."""
    return CategoryOut(
        id=category_id,
        name=name,
        servicesCount=count_services_in_category(category_id),
    )


@router.get(
    "",
    response_model=list[CategoryOut],
    summary="Список категорий услуг",
)
def get_categories() -> list[CategoryOut]:
    """Вернуть все категории услуг с количеством услуг в каждой."""
    return [_to_out(category.id, category.name) for category in list_categories()]


@router.get(
    "/{category_id}",
    response_model=CategoryDetailOut,
    responses={status.HTTP_404_NOT_FOUND: {"model": str, "description": "Category not found"}},
    summary="Информация о категории",
)
def get_category_by_id(category_id: int) -> CategoryDetailOut:
    """Вернуть категорию по id или 404 с текстом ``Category not found``."""
    category = get_category(category_id)
    if category is None:
        raise CategoryNotFoundError()

    return CategoryDetailOut(
        id=category.id,
        name=category.name,
        servicesCount=count_services_in_category(category.id),
    )
