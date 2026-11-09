# Задание 2 (следующий блок): API категорий услуг

Веб-API салона на **FastAPI**: список категорий услуг с количеством услуг и
информация о конкретной категории.

## Что реализовано

**Задание 1. Список категорий** — `GET /categories`

Возвращает массив всех категорий, у каждой есть поле `servicesCount`:

```json
[
  { "id": 1, "name": "Стрижки и укладки", "servicesCount": 5 },
  { "id": 2, "name": "Маникюр и педикюр", "servicesCount": 5 },
  { "id": 3, "name": "Брови и ресницы", "servicesCount": 4 },
  { "id": 4, "name": "Спа-процедуры", "servicesCount": 4 }
]
```

`servicesCount` не хранится в данных, а считается на лету по справочнику услуг —
поэтому он всегда актуален, даже если услугу добавили или удалили.

**Задание 2. Информация по категории** — `GET /categories/{category_id}`

- `200` — `{ "id": 1, "name": "Стрижки и укладки", "servicesCount": 5 }`
- `404` — тело ответа `Category not found`
- `422` — если `category_id` не число (стандартная валидация FastAPI)

```bash
curl -i localhost:8000/categories/999
# HTTP/1.1 404 Not Found
# content-type: text/plain; charset=utf-8
#
# Category not found
```

Чтобы 404 отдавал именно строку (а не `{"detail": "..."}`), заведены свои
исключения и обработчики в `app/errors.py`. Если клиент явно просит
`Accept: application/json`, вернётся `{"detail": "Category not found"}` —
удобно для фронтенда, при этом контракт задания не нарушается.

## Структура

```
2/
├── app/
│   ├── main.py              # создание FastAPI-приложения
│   ├── models.py            # Category, Service, Master, схемы ответов
│   ├── storage.py           # данные в памяти + подсчёт услуг
│   ├── errors.py            # доменные ошибки → HTTP-ответы
│   └── routers/
│       └── categories.py    # GET /categories, GET /categories/{id}
├── tests/
│   └── test_categories.py   # 10 тестов
├── requirements.txt
└── pyproject.toml
```

## Запуск

```bash
cd 2
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt        # Windows: .venv\Scripts\pip
.venv/bin/uvicorn app.main:app --reload --port 8000  # Windows: .venv\Scripts\uvicorn
```

- Swagger UI: <http://localhost:8000/docs>
- OpenAPI: <http://localhost:8000/openapi.json>
- Проверка живости: `GET /health` → `{"status": "ok"}`

## Тесты

```bash
cd 2
.venv/bin/python -m pytest -q      # 10 passed
```

## Пример ответа, который вернул живой сервер

```bash
$ curl -s localhost:8000/categories
[{"id":1,"name":"Стрижки и укладки","servicesCount":5},
 {"id":2,"name":"Маникюр и педикюр","servicesCount":5},
 {"id":3,"name":"Брови и ресницы","servicesCount":4},
 {"id":4,"name":"Спа-процедуры","servicesCount":4}]
```
