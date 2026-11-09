## Запуск

```bash
cd 2
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app.main:app --reload --port 8000  
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
