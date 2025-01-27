# Instant Messaging Service

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-brightgreen)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue)](https://www.docker.com/)

## Описание проекта

**Instant Messaging Service** — это веб-приложение для обмена сообщениями в реальном времени. Сервис позволяет пользователям регистрироваться, аутентифицироваться, отправлять и получать сообщения с историей чатов, а также получать уведомления через Telegram-бота.

Проект разработан с использованием стека FastAPI, WebSockets, PostgreSQL и Docker.

---

## Основные функции

- **Регистрация и аутентификация пользователей.**
- **Отправка и получение сообщений в реальном времени.**
- **Сохранение истории сообщений в базе данных PostgreSQL.**

---

## Технологии

### Backend:
- **FastAPI** — разработка RESTful API.
- **WebSockets** — реализация реального времени.
- **SQLAlchemy + Alembic** — работа с PostgreSQL и управление миграциями.


### Инфраструктура:
- **Docker** — контейнеризация приложения.

---

## Установка и запуск
   На данном этапе проект находится в стадии разработки и тестирования в ручном режиме через Postman.
   Для запуска приложения на локальной машине необходимо выполнить следующие шаги.

### Требования
- **Docker** версии 20.10+
- **Docker Compose** версии 1.29+

### Шаги для запуска
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/DarjaBalasheva/Instant-Messaging-Service.git
   cd Instant-Messaging-Service
    ```
2. Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные окружения:
    ```bash
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=postgres
    POSTGRES_HOST=db
    POSTGRES_PORT=5432

   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   TOKEN_SECRET_KEY="SECRET_KEY"
   ALGORITHM = "HS256"
    ```
3. Запустите приложение:
    ```bash
    docker-compose up --build
    ```

4. Приложение будет доступно по адресу: `localhost:8000`.
5. Документация Swagger: `localhost:8000/docs`.
