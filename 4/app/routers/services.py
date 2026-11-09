"""API услуг.

* ``POST /services``             — создать услугу (валидация через ServiceCreate);
* ``GET  /services``             — список услуг, опционально ``?categoryId=``;
* ``GET  /services/{service_id}`` — одна услуга.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Service, get_category, get_services
from app.schemas import ServiceCreate, ServiceOut, service_to_out

router = APIRouter(prefix="/services", tags=["services"])


@router.post(
    "",
    response_model=ServiceOut,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Category not found"}},
    summary="Создать услугу",
)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    """Добавить услугу в категорию.

    Некорректное тело запроса отсекает Pydantic (``422``) ещё до обращения к
    БД, поэтому в таблицу попадают только валидные записи. Если категории из
    ``categoryId`` нет — ``404 Category not found``.
    """
    if get_category(db, payload.categoryId) is None:
        return PlainTextResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Category not found",
        )

    service = Service(
        category_id=payload.categoryId,
        title=payload.title,
        desc=payload.desc,
        duration=payload.duration,
        price=payload.price,
    )
    db.add(service)
    db.commit()
    db.refresh(service)

    return service_to_out(service)


@router.get("", response_model=list[ServiceOut], summary="Список услуг")
def list_services(
    categoryId: int | None = Query(default=None, description="Фильтр по категории"),
    db: Session = Depends(get_db),
) -> list[ServiceOut]:
    return [service_to_out(service) for service in get_services(db, categoryId)]


@router.get(
    "/{service_id}",
    response_model=ServiceOut,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Service not found"}},
    summary="Услуга по id",
)
def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if service is None:
        return PlainTextResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Service not found",
        )
    return service_to_out(service)
