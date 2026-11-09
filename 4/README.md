## Запуск

```bash
cd 4
python -m venv .venv
.venv/Scripts/pip install -r requirements-dev.txt
.venv/Scripts/uvicorn app.main:app --reload --port 8003
```

- Swagger UI: <http://localhost:8003/docs> — там же удобно отправлять POST.
- Файл `salon.db` создаётся автоматически и в git не попадает.
- Другая БД: `DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/salon`.

## Тесты

```bash
cd 4
.venv/bin/python -m pytest -q      # 39 passed
```
