"""Учебный мини-проект «Салон красоты».

Публичный API пакета::

    from salon import Appointment, create_appointment, appointments
"""

from salon.models import (
    WORKING_DAY_END,
    WORKING_DAY_START,
    Appointment,
    Master,
    Service,
    ValidationError,
)
from salon.services import create_appointment
from salon.storage import appointments, get_master, get_service, reset_appointments

__all__ = [
    "Appointment",
    "Master",
    "Service",
    "ValidationError",
    "WORKING_DAY_START",
    "WORKING_DAY_END",
    "appointments",
    "create_appointment",
    "get_master",
    "get_service",
    "reset_appointments",
]
