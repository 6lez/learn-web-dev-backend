"""Тесты модели Master и API мастеров."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from sqlalchemy import create_engine

from app.database import Base
from app.models import Master


# --- Задание 1. Модель и таблица ------------------------------------------


def test_masters_table_has_required_columns(tmp_path) -> None:
    test_engine = create_engine(f"sqlite:///{tmp_path / 'masters.db'}")
    Base.metadata.create_all(bind=test_engine)

    columns = {column["name"] for column in inspect(test_engine).get_columns("masters")}
    assert {"id", "name", "specialization"} <= columns
    assert Master.__tablename__ == "masters"

    test_engine.dispose()


def test_master_model_roundtrip(db_session: Session) -> None:
    master = Master(name="Светлана", specialization="Косметолог")
    db_session.add(master)
    db_session.commit()

    saved = db_session.get(Master, master.id)
    assert saved is not None
    assert (saved.name, saved.specialization) == ("Светлана", "Косметолог")


def test_master_name_and_specialization_are_required(db_session: Session) -> None:
    from sqlalchemy.exc import IntegrityError

    db_session.add(Master(name=None, specialization="Парикмахер"))  # type: ignore[arg-type]
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


# --- Задание 2. API -------------------------------------------------------


def test_get_all_masters(client: TestClient) -> None:
    response = client.get("/masters")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Анна", "specialization": "Парикмахер"},
        {"id": 2, "name": "Мария", "specialization": "Визажист"},
        {"id": 3, "name": "Игорь", "specialization": "Парикмахер"},
    ]


def test_filter_by_specialization(client: TestClient) -> None:
    response = client.get("/masters", params={"specialization": "Парикмахер"})

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Анна", "specialization": "Парикмахер"},
        {"id": 3, "name": "Игорь", "specialization": "Парикмахер"},
    ]


def test_filter_by_unknown_specialization_returns_empty_list(client: TestClient) -> None:
    response = client.get("/masters", params={"specialization": "Стоматолог"})

    assert response.status_code == 200
    assert response.json() == []


def test_get_master_by_id(client: TestClient) -> None:
    response = client.get("/masters/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Анна",
        "specialization": "Парикмахер",
    }


def test_get_missing_master_returns_404(client: TestClient) -> None:
    response = client.get("/masters/999")

    assert response.status_code == 404
    assert response.text == "Master not found"


def test_get_master_with_non_integer_id_returns_422(client: TestClient) -> None:
    assert client.get("/masters/abc").status_code == 422


def test_new_master_appears_in_list(client: TestClient, db_session: Session) -> None:
    db_session.add(Master(name="Мария", specialization="Визажист"))
    db_session.commit()

    masters = client.get("/masters").json()
    assert len(masters) == 4
    assert masters[-1] == {"id": 4, "name": "Мария", "specialization": "Визажист"}
