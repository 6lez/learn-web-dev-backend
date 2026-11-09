"""Бизнес-логика салона: создание записи клиента."""

from __future__ import annotations

from salon.models import Appointment, ValidationError
from salon.storage import appointments, get_master, get_service


def _is_slot_taken(master_id: int, time: str) -> bool:
    """Занято ли указанное время у конкретного мастера."""
    return any(
        appointment.master_id == master_id and appointment.time == time
        for appointment in appointments
    )


def create_appointment(
    client_name: str,
    master_id: int,
    service_id: int,
    time: str,
) -> Appointment | None:
    """Создать запись клиента к мастеру.

    Возвращает объект :class:`Appointment`, если все поля заполнены корректно,
    и ``None``, если:

    * мастер или услуга не найдены;
    * хотя бы одно поле заполнено неверно (пустое имя, время вне часов работы
      салона с 08:00 до 20:00 и т.п.);
    * у выбранного мастера это время уже занято.

    Неудачная попытка записи никак не меняет список ``appointments``.
    """
    master = get_master(master_id)
    service = get_service(service_id)

    if master is None or service is None:
        return None

    try:
        appointment = Appointment(
            appointment_id=0,  # настоящий id выдадим ниже, когда запись валидна
            client_name=client_name,
            master_id=master.master_id,
            service_id=service.service_id,
            time=time,
        )
    except ValidationError:
        # Объект не создан — значит, и в списке записей ничего не появилось.
        return None

    if _is_slot_taken(appointment.master_id, appointment.time):
        return None

    appointment.appointment_id = len(appointments) + 1
    appointments.append(appointment)
    return appointment
