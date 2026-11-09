"""Справочники и «база данных» в памяти.

В настоящем проекте здесь были бы запросы к БД, но для учебного задания
достаточно обычных списков и словарей.
"""

from __future__ import annotations

from salon.models import Appointment, Master, Service

# Список всех записей. Именно его проверяют тесты из задания.
appointments: list[Appointment] = []

MASTERS: dict[int, Master] = {
    1: Master(1, "Анна Смирнова", "парикмахер-стилист"),
    2: Master(2, "Ольга Кузнецова", "мастер маникюра"),
    3: Master(3, "Игорь Петров", "барбер"),
}

SERVICES: dict[int, Service] = {
    1: Service(1, "Стрижка и укладка", 3500.0),
    2: Service(2, "Маникюр", 2500.0),
    3: Service(3, "Мужская стрижка", 2000.0),
}


def get_master(master_id: int) -> Master | None:
    """Вернуть мастера по идентификатору или ``None``, если такого нет."""
    return MASTERS.get(master_id)


def get_service(service_id: int) -> Service | None:
    """Вернуть услугу по идентификатору или ``None``, если такой нет."""
    return SERVICES.get(service_id)


def reset_appointments() -> None:
    """Очистить список записей (удобно между прогонами тестов и демо)."""
    appointments.clear()
