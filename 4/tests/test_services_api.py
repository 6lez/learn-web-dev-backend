"""Задание 2: POST /services — ровно сценарии проверки из задания."""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Service

PAYLOAD = {
    "categoryId": 3,
    "title": "Наращивание ресниц",
    "desc": "Огромные ресницы уже через 30 минут",
    "duration": 30,
    "price": 1500.00,
}


# --- Проверка 1: успешное создание ----------------------------------------


def test_create_service_returns_201(client: TestClient, db_session: Session) -> None:
    response = client.post("/services", json=PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["categoryId"] == 3
    assert body["title"] == "Наращивание ресниц"
    assert body["desc"] == "Огромные ресницы уже через 30 минут"
    assert body["duration"] == 30
    assert body["price"] == 1500.00

    # Запись действительно попала в БД.
    saved = db_session.get(Service, body["id"])
    assert saved is not None
    assert saved.category_id == 3
    assert str(saved.price) == "1500.00"


def test_created_service_is_visible_in_list(client: TestClient) -> None:
    created = client.post("/services", json=PAYLOAD).json()

    services = client.get("/services").json()
    assert services == [created]

    assert client.get("/services", params={"categoryId": 3}).json() == [created]
    assert client.get("/services", params={"categoryId": 1}).json() == []


# --- Проверка 2: price = "бесплатно" -> 422 --------------------------------


def test_non_numeric_price_returns_422(client: TestClient, db_session: Session) -> None:
    response = client.post("/services", json={**PAYLOAD, "price": "бесплатно"})

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "price"]
    assert db_session.query(Service).count() == 0


# --- Проверка 3: пустой desc, duration 0, price -1500 -> 422 --------------


def test_empty_desc_zero_duration_negative_price_returns_422(
    client: TestClient, db_session: Session
) -> None:
    response = client.post(
        "/services",
        json={**PAYLOAD, "desc": "", "duration": 0, "price": -1500.00},
    )

    assert response.status_code == 422
    invalid_fields = {error["loc"][-1] for error in response.json()["detail"]}
    assert invalid_fields == {"desc", "duration", "price"}
    assert db_session.query(Service).count() == 0


# --- Прочие правила -------------------------------------------------------


def test_unknown_category_returns_404(client: TestClient, db_session: Session) -> None:
    response = client.post("/services", json={**PAYLOAD, "categoryId": 999})

    assert response.status_code == 404
    assert response.text == "Category not found"
    assert db_session.query(Service).count() == 0


def test_short_title_returns_422(client: TestClient) -> None:
    assert client.post("/services", json={**PAYLOAD, "title": ""}).status_code == 422


def test_long_desc_returns_422(client: TestClient) -> None:
    response = client.post("/services", json={**PAYLOAD, "desc": "я" * 101})

    assert response.status_code == 422


def test_duration_over_three_hours_returns_422(client: TestClient) -> None:
    assert client.post("/services", json={**PAYLOAD, "duration": 181}).status_code == 422


def test_white_space_is_trimmed(client: TestClient) -> None:
    response = client.post("/services", json={**PAYLOAD, "title": "  Стрижка  "})

    assert response.status_code == 201
    assert response.json()["title"] == "Стрижка"


def test_get_service_by_id(client: TestClient) -> None:
    created = client.post("/services", json=PAYLOAD).json()

    assert client.get(f"/services/{created['id']}").json() == created
    assert client.get("/services/999").status_code == 404
