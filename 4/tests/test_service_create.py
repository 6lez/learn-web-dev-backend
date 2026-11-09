"""Задание 1: ограничения Pydantic-модели ServiceCreate."""

from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas import ServiceCreate

VALID = {
    "categoryId": 3,
    "title": "Наращивание ресниц",
    "desc": "Огромные ресницы уже через 30 минут",
    "duration": 30,
    "price": 1500.00,
}


def test_valid_payload_is_accepted() -> None:
    service = ServiceCreate(**VALID)

    assert service.categoryId == 3
    assert service.title == "Наращивание ресниц"
    assert service.duration == 30
    assert service.price == Decimal("1500.00")


def test_price_as_string_is_coerced() -> None:
    assert ServiceCreate(**{**VALID, "price": "1500.00"}).price == Decimal("1500.00")


@pytest.mark.parametrize("field_name", ["title", "desc"])
@pytest.mark.parametrize("value", ["", "   ", "\n\t"])
def test_title_and_desc_cannot_be_empty(field_name: str, value: str) -> None:
    with pytest.raises(ValidationError) as error:
        ServiceCreate(**{**VALID, field_name: value})

    assert error.value.errors()[0]["type"] == "string_too_short"


@pytest.mark.parametrize("field_name", ["title", "desc"])
def test_title_and_desc_max_length_is_100(field_name: str) -> None:
    ServiceCreate(**{**VALID, field_name: "я" * 100})  # ровно 100 — можно

    with pytest.raises(ValidationError) as error:
        ServiceCreate(**{**VALID, field_name: "я" * 101})
    assert error.value.errors()[0]["type"] == "string_too_long"


@pytest.mark.parametrize("duration", [30, 60, 180])
def test_valid_duration(duration: int) -> None:
    assert ServiceCreate(**{**VALID, "duration": duration}).duration == duration


@pytest.mark.parametrize("duration", [0, 29, 181, 500, -30])
def test_duration_out_of_range(duration: int) -> None:
    with pytest.raises(ValidationError):
        ServiceCreate(**{**VALID, "duration": duration})


@pytest.mark.parametrize("price", [0, 0.0, -1500.00, "-0.01"])
def test_price_must_be_greater_than_zero(price: object) -> None:
    with pytest.raises(ValidationError):
        ServiceCreate(**{**VALID, "price": price})


@pytest.mark.parametrize("price", ["бесплатно", "много", None, [1500]])
def test_price_must_be_a_number(price: object) -> None:
    with pytest.raises(ValidationError) as error:
        ServiceCreate(**{**VALID, "price": price})

    assert error.value.errors()[0]["type"] in {
        "decimal_parsing",
        "decimal_type",
        "string_type",
        "int_type",
        "int_parsing",
        "float_type",
        "float_parsing",
    }


def test_category_id_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        ServiceCreate(**{**VALID, "categoryId": 0})


def test_missing_fields_are_reported() -> None:
    with pytest.raises(ValidationError) as error:
        ServiceCreate(**{k: v for k, v in VALID.items() if k != "title"})

    assert error.value.errors()[0]["loc"] == ("title",)


def test_extra_fields_are_forbidden() -> None:
    with pytest.raises(ValidationError):
        ServiceCreate(**{**VALID, "unknown": 1})
