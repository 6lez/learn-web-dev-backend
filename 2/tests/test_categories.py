"""Тесты эндпоинтов категорий (задания 3 и 4)."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import CATEGORIES, SERVICES

client = TestClient(app)


# --- Задание 1. Список категорий ------------------------------------------


def test_get_categories_returns_all_categories() -> None:
    response = client.get("/categories")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == len(CATEGORIES)
    assert body == [
        {"id": 1, "name": "Стрижки и укладки", "servicesCount": 5},
        {"id": 2, "name": "Маникюр и педикюр", "servicesCount": 5},
        {"id": 3, "name": "Брови и ресницы", "servicesCount": 4},
        {"id": 4, "name": "Спа-процедуры", "servicesCount": 4},
    ]


def test_every_category_has_services_count_field() -> None:
    for category in client.get("/categories").json():
        assert set(category) == {"id", "name", "servicesCount"}
        assert category["servicesCount"] == sum(
            1 for service in SERVICES.values() if service.category_id == category["id"]
        )


# --- Задание 2. Информация по категории -----------------------------------


def test_get_category_by_id() -> None:
    response = client.get("/categories/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Стрижки и укладки",
        "servicesCount": 5,
    }


def test_get_unknown_category_returns_404_with_text() -> None:
    response = client.get("/categories/999")

    assert response.status_code == 404
    assert response.text == "Category not found"


def test_get_unknown_category_returns_json_when_requested() -> None:
    response = client.get("/categories/999", headers={"Accept": "application/json"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test_get_category_with_non_integer_id() -> None:
    response = client.get("/categories/abc")

    assert response.status_code == 422


@pytest.mark.parametrize("category_id", sorted(CATEGORIES))
def test_category_detail_matches_list_item(category_id: int) -> None:
    list_item = next(
        item for item in client.get("/categories").json() if item["id"] == category_id
    )
    detail = client.get(f"/categories/{category_id}").json()

    assert detail == list_item
