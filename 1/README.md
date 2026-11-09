```
├── 1/   # Задание 1. Класс Appointment + часы работы салона (чистый Python)
└── 2/   # Задание 2. API категорий услуг (FastAPI)
```

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
