"""SQLAlchemy-модели и схемы ответов API."""

from __future__ import annotations

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.database import Base


class Master(Base):
    """Мастер салона — таблица ``masters``.

    Поля:

    * ``id``             — первичный ключ;
    * ``name``           — имя мастера;
    * ``specialization`` — специализация (Парикмахер, Визажист, ...).
    """

    __tablename__ = "masters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    specialization: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    def __repr__(self) -> str:
        return (
            f"Master(id={self.id!r}, name={self.name!r}, "
            f"specialization={self.specialization!r})"
        )


def get_masters(db: Session, specialization: str | None = None) -> list[Master]:
    """Все мастера, опционально — только с указанной специализацией."""
    query = select(Master).order_by(Master.id)
    if specialization is not None:
        query = query.where(Master.specialization == specialization)
    return list(db.scalars(query).all())


def get_master(db: Session, master_id: int) -> Master | None:
    """Мастер по id или ``None``."""
    return db.get(Master, master_id)
