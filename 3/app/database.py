"""Подключение к БД и базовая модель SQLAlchemy."""

from __future__ import annotations

import os
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# По умолчанию SQLite-файл рядом с проектом. В тестах подменяется на in-memory.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./salon.db")

engine = create_engine(
    DATABASE_URL,
    # check_same_thread=False нужен для SQLite: FastAPI обслуживает запросы в разных потоках.
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Базовый класс всех моделей проекта."""


def get_db() -> Iterator[Session]:
    """Зависимость FastAPI: сессия БД на время одного запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
