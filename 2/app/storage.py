"""Данные в памяти вместо БД: справочники категорий, услуг и мастеров."""

from __future__ import annotations

from app.models import Category, Master, Service

CATEGORIES: dict[int, Category] = {
    1: Category(1, "Стрижки и укладки"),
    2: Category(2, "Маникюр и педикюр"),
    3: Category(3, "Брови и ресницы"),
    4: Category(4, "Спа-процедуры"),
}

SERVICES: dict[int, Service] = {
    1: Service(1, "Женская стрижка", 1, 3500.0, 60),
    2: Service(2, "Мужская стрижка", 1, 2000.0, 45),
    3: Service(3, "Укладка", 1, 2500.0, 45),
    4: Service(4, "Окрашивание", 1, 6500.0, 120),
    5: Service(5, "Детская стрижка", 1, 1500.0, 30),
    6: Service(6, "Классический маникюр", 2, 2500.0, 60),
    7: Service(7, "Педикюр", 2, 3500.0, 90),
    8: Service(8, "Наращивание ногтей", 2, 4500.0, 120),
    9: Service(9, "Покрытие гель-лак", 2, 2000.0, 60),
    10: Service(10, "Спа-уход для рук", 2, 1800.0, 45),
    11: Service(11, "Коррекция бровей", 3, 1500.0, 30),
    12: Service(12, "Окрашивание бровей", 3, 1200.0, 30),
    13: Service(13, "Ламинирование бровей", 3, 2200.0, 60),
    14: Service(14, "Наращивание ресниц", 3, 3000.0, 120),
    15: Service(15, "Массаж лица", 4, 2800.0, 45),
    16: Service(16, "Обёртывание", 4, 4000.0, 60),
    17: Service(17, "Пилинг", 4, 3200.0, 45),
    18: Service(18, "Уходовая маска", 4, 2000.0, 30),
}

MASTERS: dict[int, Master] = {
    1: Master(1, "Анна Смирнова", "парикмахер-стилист"),
    2: Master(2, "Ольга Кузнецова", "мастер маникюра"),
    3: Master(3, "Игорь Петров", "барбер"),
}


def get_category(category_id: int) -> Category | None:
    return CATEGORIES.get(category_id)


def list_categories() -> list[Category]:
    return list(CATEGORIES.values())


def services_of_category(category_id: int) -> list[Service]:
    """Все услуги конкретной категории."""
    return [s for s in SERVICES.values() if s.category_id == category_id]


def count_services_in_category(category_id: int) -> int:
    """servicesCount для категории."""
    return len(services_of_category(category_id))


def get_master(master_id: int) -> Master | None:
    return MASTERS.get(master_id)


def get_service(service_id: int) -> Service | None:
    return SERVICES.get(service_id)
