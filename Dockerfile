
FROM python:3.12-slim

LABEL authors="Игорь"

# Установка рабочего каталога
WORKDIR /app

# Установка необходимых системных зависимостей и poetry
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

# Обновление PATH и переменная часового пояса
ENV PATH="/root/.local/bin:$PATH" \
    TZ=Europe/Moscow

# Установка часового пояса контейнера
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Копирование файлов для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry install --no-root --no-dev

# Копирование исходного кода
COPY . .

EXPOSE 8000

# Запуск uvicorn сервера
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
