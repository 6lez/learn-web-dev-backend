"""Общие фикстуры: отдельная in-memory БД на каждый тест."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Master


@pytest.fixture()
def db_session() -> Iterator[Session]:
    """Пустая БД в памяти с тремя мастерами."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        # Одно общее соединение — иначе каждая сессия получила бы пустую БД.
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, expire_on_commit=False
    )

    with TestingSessionLocal() as session:
        session.add_all(
            [
                Master(id=1, name="Анна", specialization="Парикмахер"),
                Master(id=2, name="Мария", specialization="Визажист"),
                Master(id=3, name="Игорь", specialization="Парикмахер"),
            ]
        )
        session.commit()
        yield session

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def client(db_session: Session) -> Iterator[TestClient]:
    """Клиент API, у которого get_db смотрит в тестовую БД."""

    def override_get_db() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    # Без `with`: lifespan (создание реального файла salon.db) в тестах не нужен.
    yield TestClient(app)
    app.dependency_overrides.clear()
