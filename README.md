| Папка | Что внутри | Стек | Запуск |
|-------|------------|------|--------|
| [`1/`](1/README.md) | Класс `Appointment` вместо словаря, правило «запись только с 08:00 до 20:00» | Python 3.10+ | `cd 1 && python -m salon.demo` · `.venv/bin/python -m pytest -q` |
| [`2/`](2/README.md) | `GET /categories`, `GET /categories/{category_id}` | FastAPI | `cd 2 && .venv/bin/uvicorn app.main:app --reload --port 8000` |
| [`3/`](3/README.md) | Модель `Master` и таблица `masters`, `GET /masters`, `/masters?specialization=…`, `/masters/{id}` | FastAPI + SQLAlchemy + SQLite | `cd 3 && .venv/bin/uvicorn app.main:app --reload --port 8002` |
| [`4/`](4/README.md) | Pydantic-модель `ServiceCreate` с ограничениями, `POST /services`, `GET /services` | FastAPI + Pydantic + SQLAlchemy | `cd 4 && .venv/bin/uvicorn app.main:app --reload --port 8003` |

```bash
# Задание 1
cd 1
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q

# Задание 2
cd ../2
python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q

# Задание 3
cd ../3
python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q

# Задание 4
cd ../4
python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
```

> Windows: пути к исполняемым файлам в venv — `.venv\Scripts\python`,
> `.venv\Scripts\pip`, `.venv\Scripts\uvicorn`.