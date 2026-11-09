"""Приложение салона: категории услуг, услуги и записи клиентов."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Category:
    """Категория услуг, например «Стрижки и укладки»."""

    id: int
    name: str


@dataclass(frozen=True)
class Service:
    """Услуга салона. Каждая услуга принадлежит одной категории."""

    id: int
    name: str
    category_id: int
    price: float = 0.0
    duration_minutes: int = 60


@dataclass(frozen=True)
class Master:
    """Мастер салона."""

    id: int
    full_name: str
    specialization: str = ""


@dataclass(frozen=True)
class Appointment:
    """Запись клиента (из задания 1)."""

    id: int
    client_name: str
    master_id: int
    service_id: int
    time: str


# --- Схемы ответов API -----------------------------------------------------


@dataclass(frozen=True)
class CategoryOut:
    """Категория с количеством услуг в ней — то, что отдаёт API."""

    id: int
    name: str
    servicesCount: int  # noqa: N815 — имя поля должно совпадать с контрактом API


@dataclass(frozen=True)
class CategoryDetailOut:
    """Информация о конкретной категории."""

    id: int
    name: str
    servicesCount: int  # noqa: N815


@dataclass(frozen=True)
class ServiceOut:
    id: int
    name: str
    category_id: int  # noqa: N815
    price: float
    duration_minutes: int


@dataclass(frozen=True)
class ErrorOut:
    """Тело ошибки в едином формате."""

    detail: str


@dataclass
class ReservationOut:
    """Упрощённая запись клиента для демонстрации."""

    id: int
    client_name: str
    master_id: int
    service_id: int
    time: str
    tags: list[str] = field(default_factory=list)
