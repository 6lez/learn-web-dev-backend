# Практические задания: Python + backend

Задания сгруппированы по папкам — каждое задание в своей директории со своим
README, зависимостями и тестами.

```
.
├── 1/   # Задание 1. Класс Appointment + часы работы салона (чистый Python)
└── 2/   # Задание 2. API категорий услуг (FastAPI)
```

| Папка | Что внутри | Стек | Запуск |
|-------|------------|------|--------|
| [`1/`](1/README.md) | Класс `Appointment` вместо словаря, правило «запись только с 08:00 до 20:00» | Python 3.10+ | `cd 1 && python -m salon.demo` · `.venv/bin/python -m pytest -q` |
| [`2/`](2/README.md) | `GET /categories`, `GET /categories/{category_id}` | FastAPI + uvicorn | `cd 2 && .venv/bin/uvicorn app.main:app --reload --port 8000` |

Папки независимы: у каждой свой `requirements.txt`, `pyproject.toml` и `.venv`,
поэтому можно запускать и проверять их по отдельности.

## Быстрая проверка

```bash
# Задание 1
cd 1
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q
python -m salon.demo

# Задание 2
cd ../2
python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
.venv/bin/uvicorn app.main:app --reload --port 8000
```

> Windows: пути к исполняемым файлам в venv — `.venv\Scripts\python`,
> `.venv\Scripts\pip`, `.venv\Scripts\uvicorn`.
