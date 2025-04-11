FROM python:3.12-slim

# переменные среды
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# раб директория
WORKDIR /app

# Poetry
RUN pip install --upgrade pip && pip install poetry

# копирую файлы зависимостей и устанавливаю их
COPY pyproject.toml poetry.lock /app/
RUN poetry install --without dev --no-root

# копирую всё остальное приложение
COPY . /app

# можно сразу применять миграции,если это нужно при старте
# RUN poetry run alembic upgrade head

# запуск приложение на 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

