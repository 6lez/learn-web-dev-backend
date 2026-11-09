"""Pydantic-схемы: что именно уходит клиенту в JSON."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MasterOut(BaseModel):
    """Мастер в ответе API."""

    # from_attributes позволяет собирать схему прямо из ORM-объекта.
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Анна"])
    specialization: str = Field(..., examples=["Парикмахер"])
