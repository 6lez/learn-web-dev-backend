"""Модели предметной области салона красоты.

Здесь живут три сущности:

* ``Master``      — мастер;
* ``Service``     — услуга;
* ``Appointment`` — запись клиента (главный герой задания 1).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from datetime import time as Time

# Бизнес-правило задания 2: записаться можно только в часы работы салона.
WORKING_DAY_START = Time(8, 0)
WORKING_DAY_END = Time(20, 0)

TIME_FORMAT = "%H:%M"


class ValidationError(ValueError):
    """Данные записи некорректны, объект создать нельзя."""


@dataclass(frozen=True)
class Master:
    """Мастер салона."""

    master_id: int
    full_name: str
    specialization: str = ""


@dataclass(frozen=True)
class Service:
    """Услуга салона."""

    service_id: int
    title: str
    price: float = 0.0


class Appointment:
    """Запись клиента к мастеру.

    Объект можно создать только из полностью и корректно заполненных полей:
    любой невалидный аргумент приводит к ``ValidationError``, и объект
    не появляется на свет.

    >>> Appointment(1, "Иванова А.А.", 1, 1, "10:00").time
    '10:00'
    >>> Appointment(2, "", 1, 1, "10:00")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    salon.models.ValidationError: Не заполнено поле client_name
    """

    def __init__(
        self,
        appointment_id: int,
        client_name: str,
        master_id: int,
        service_id: int,
        time: str,
    ) -> None:
        # Сначала проверяем все поля...
        validated_client_name = self._validate_client_name(client_name)
        validated_master_id = self._validate_id(master_id, "master_id")
        validated_service_id = self._validate_id(service_id, "service_id")
        validated_time = self._validate_time(time)

        # ...и только потом сохраняем их в объект.
        self.appointment_id = appointment_id
        self.client_name = validated_client_name
        self.master_id = validated_master_id
        self.service_id = validated_service_id
        self.time = validated_time

    @staticmethod
    def _validate_client_name(client_name: str) -> str:
        if not isinstance(client_name, str) or not client_name.strip():
            raise ValidationError("Не заполнено поле client_name")
        return client_name.strip()

    @staticmethod
    def _validate_id(value: int, field_name: str) -> int:
        # bool — подкласс int, поэтому True/False идентификатором быть не может.
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValidationError(f"Не заполнено или некорректно поле {field_name}")
        return value

    @staticmethod
    def _validate_time(value: str) -> str:
        """Проверить время: формат ``HH:MM`` и часы работы салона."""
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Не заполнено поле time")

        try:
            parsed = datetime.strptime(value.strip(), TIME_FORMAT).time()
        except ValueError as error:
            raise ValidationError(
                f"Время должно быть в формате HH:MM, получено: {value!r}"
            ) from error

        if not WORKING_DAY_START <= parsed < WORKING_DAY_END:
            raise ValidationError(
                "Салон работает с "
                f"{WORKING_DAY_START.strftime(TIME_FORMAT)} до "
                f"{WORKING_DAY_END.strftime(TIME_FORMAT)}. "
                f"Запись на {value} невозможна"
            )

        return parsed.strftime(TIME_FORMAT)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Appointment):
            return NotImplemented
        return (
            self.appointment_id,
            self.client_name,
            self.master_id,
            self.service_id,
            self.time,
        ) == (
            other.appointment_id,
            other.client_name,
            other.master_id,
            other.service_id,
            other.time,
        )

    def __repr__(self) -> str:
        return (
            f"Appointment(appointment_id={self.appointment_id!r}, "
            f"client_name={self.client_name!r}, "
            f"master_id={self.master_id!r}, "
            f"service_id={self.service_id!r}, "
            f"time={self.time!r})"
        )
