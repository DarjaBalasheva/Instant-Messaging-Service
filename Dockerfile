FROM python:3.12

# Установка зависимостей системы
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Установка pipenv и fastapi-cache2 с поддержкой Redis
RUN pip install pipenv "fastapi-cache2[redis]"

WORKDIR /app

RUN pipenv lock

COPY Pipfile Pipfile.lock ./

# Установка зависимостей с помощью pipenv
RUN pipenv install --system --deploy

COPY . .

#RUN alembic upgrade head

# Запуск приложения FastAPI
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
