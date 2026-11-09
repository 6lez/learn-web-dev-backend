"""Тесты для заданий 1 и 2."""

import pytest

from salon import appointments, create_appointment, reset_appointments
from salon.models import Appointment, ValidationError


@pytest.fixture(autouse=True)
def clean_appointments() -> None:
    """Перед каждым тестом список записей пуст."""
    reset_appointments()
    yield
    reset_appointments()


# --- Задание 1: класс Appointment ------------------------------------------


def test_create_appointment_returns_appointment_object() -> None:
    first = create_appointment("Иванова А.А.", 1, 1, "10:00")
    second = create_appointment("Петрова А.А.", 1, 1, "11:00")

    assert isinstance(first, Appointment)
    assert isinstance(second, Appointment)
    assert appointments == [first, second]
    assert [(a.client_name, a.time) for a in appointments] == [
        ("Иванова А.А.", "10:00"),
        ("Петрова А.А.", "11:00"),
    ]


def test_ids_are_sequential() -> None:
    first = create_appointment("Иванова А.А.", 1, 1, "10:00")
    second = create_appointment("Петрова А.А.", 1, 1, "11:00")

    assert first is not None and second is not None
    assert (first.appointment_id, second.appointment_id) == (1, 2)


def test_empty_client_name_creates_nothing() -> None:
    result = create_appointment("", 1, 1, "12:00")

    assert result is None
    assert len(appointments) == 0


@pytest.mark.parametrize("client_name", ["", "   ", None, 123])
def test_invalid_client_name_creates_nothing(client_name: object) -> None:
    assert create_appointment(client_name, 1, 1, "12:00") is None  # type: ignore[arg-type]
    assert appointments == []


def test_unknown_master_or_service_creates_nothing() -> None:
    assert create_appointment("Иванова А.А.", 99, 1, "10:00") is None
    assert create_appointment("Иванова А.А.", 1, 99, "10:00") is None
    assert appointments == []


def test_appointment_class_validates_fields_directly() -> None:
    with pytest.raises(ValidationError):
        Appointment(1, "", 1, 1, "10:00")

    with pytest.raises(ValidationError):
        Appointment(1, "Иванова А.А.", 0, 1, "10:00")

    appointment = Appointment(1, "  Иванова А.А.  ", 1, 1, "10:00")
    assert appointment.client_name == "Иванова А.А."


# --- Задание 2: часы работы салона ----------------------------------------


@pytest.mark.parametrize("time", ["00:00", "07:59", "20:00", "23:59"])
def test_time_outside_working_hours_creates_nothing(time: str) -> None:
    assert create_appointment("Сидорова А.А.", 1, 1, time) is None
    assert len(appointments) == 0


@pytest.mark.parametrize("time", ["08:00", "12:30", "19:59"])
def test_time_inside_working_hours_is_allowed(time: str) -> None:
    assert create_appointment("Сидорова А.А.", 1, 1, time) is not None
    assert len(appointments) == 1


@pytest.mark.parametrize("time", ["", "25:00", "10-00", "abc"])
def test_invalid_time_format_creates_nothing(time: str) -> None:
    assert create_appointment("Сидорова А.А.", 1, 1, time) is None
    assert appointments == []


def test_same_master_same_time_is_rejected() -> None:
    assert create_appointment("Иванова А.А.", 1, 1, "10:00") is not None
    assert create_appointment("Петрова А.А.", 1, 2, "10:00") is None
    assert len(appointments) == 1


def test_different_masters_same_time_is_allowed() -> None:
    assert create_appointment("Иванова А.А.", 1, 1, "10:00") is not None
    assert create_appointment("Петрова А.А.", 2, 2, "10:00") is not None
    assert len(appointments) == 2
