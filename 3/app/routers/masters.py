"""API мастеров.

* ``GET /masters``                            — все мастера;
* ``GET /masters?specialization=Парикмахер``  — мастера нужной специализации;
* ``GET /masters/{master_id}``                — один мастер или 404.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import get_master, get_masters
from app.schemas import MasterOut

router = APIRouter(prefix="/masters", tags=["masters"])


@router.get("", response_model=list[MasterOut], summary="Список мастеров")
def list_masters(
    specialization: str | None = Query(
        default=None,
        description="Фильтр по специализации, например «Парикмахер»",
    ),
    db: Session = Depends(get_db),
) -> list[MasterOut]:
    """Вернуть всех мастеров из БД, при необходимости — одной специализации."""
    masters = get_masters(db, specialization=specialization)
    return [MasterOut.model_validate(master) for master in masters]


@router.get(
    "/{master_id}",
    response_model=MasterOut,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Master not found"}},
    summary="Мастер по id",
)
def get_master_by_id(
    master_id: int,
    db: Session = Depends(get_db),
):
    """Вернуть мастера по id или 404, если его нет в таблице."""
    master = get_master(db, master_id)
    if master is None:
        return PlainTextResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Master not found",
        )
    return MasterOut.model_validate(master)
