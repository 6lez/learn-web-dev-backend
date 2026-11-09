## Запуск

```bash
cd 3
python -m venv .venv
.venv/Scripts/pip install -r requirements-dev.txt
.venv/Scripts/uvicorn app.main:app --reload --port 8002
```

- Swagger UI: <http://localhost:8002/docs>
- Файл БД `salon.db` создаётся автоматически и в git не попадает.

Своя БД, например PostgreSQL, подключается переменной окружения
`DATABASE_URL`:

```bash
DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/salon uvicorn app.main:app
```

## Тесты

```bash
cd 3
.venv/bin/python -m pytest -q
```