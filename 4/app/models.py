"""SQLAlchemy-модели: категории и услуги."""

from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Text, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from app.database import Base


class Category(Base):
    """Категория услуг — таблица ``categories``."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    services: Mapped[list["Service"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r})"


class Service(Base):
    """Услуга салона — таблица ``services``.

    Ограничения продублированы на уровне БД, чтобы некорректная запись не
    попала в таблицу даже в обход API.
    """

    __tablename__ = "services"
    __table_args__ = (
        CheckConstraint("duration >= 30 AND duration <= 180", name="ck_services_duration"),
        CheckConstraint("price > 0", name="ck_services_price"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    desc: Mapped[str] = mapped_column(String(100), nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False, comment="минуты, 30..180")
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    category: Mapped[Category] = relationship(back_populates="services")

    def __repr__(self) -> str:
        return (
            f"Service(id={self.id!r}, category_id={self.category_id!r}, "
            f"title={self.title!r}, duration={self.duration!r}, price={self.price!r})"
        )


def get_category(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)


def get_services(db: Session, category_id: int | None = None) -> list[Service]:
    query = select(Service).order_by(Service.id)
    if category_id is not None:
        query = query.where(Service.category_id == category_id)
    return list(db.scalars(query).all())
