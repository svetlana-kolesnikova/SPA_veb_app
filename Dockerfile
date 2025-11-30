# Базовый образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install poetry

# Создаём рабочую директорию
WORKDIR /app

# Копируем только pyproject.toml для кеширования зависимостей
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости без виртуального окружения
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копируем весь проект
COPY . /app

# Открываем порт
EXPOSE 8000

# Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
