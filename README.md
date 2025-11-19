# DayScope

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/) [![aiogram](https://img.shields.io/badge/aiogram-3.18.0-5DADE2.svg)](https://docs.aiogram.dev/) [![aiogram-dialog](https://img.shields.io/badge/aiogram--dialog-2.3.1-9B59B6.svg)](https://aiogram-dialog.readthedocs.io/) [![fluentogram](https://img.shields.io/badge/fluentogram-1.1.10-16A085.svg)](https://pypi.org/project/fluentogram/) [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.41-F39C12.svg)](https://docs.sqlalchemy.org/) [![Alembic](https://img.shields.io/badge/Alembic-1.16.2-27AE60.svg)](https://alembic.sqlalchemy.org/) [![Redis](https://img.shields.io/badge/Redis-6.2.0-E74C3C.svg)](https://redis.io/) [![Dynaconf](https://img.shields.io/badge/Dynaconf-3.2.11-1ABC9C.svg)](https://www.dynaconf.com/) [![structlog](https://img.shields.io/badge/structlog-25.4.0-FD79A8.svg)](https://www.structlog.org/)

DayScope — удобный Telegram-бот, который помогает формировать и отслеживать привычки.

- [aiogram](https://docs.aiogram.dev/en/latest/) — Асинхронный фреймворк для Telegram-ботов
- [aiogram-dialog](https://aiogram-dialog.readthedocs.io/en/latest/) — Менеджер диалогов для aiogram
- [SQLAlchemy](https://docs.sqlalchemy.org/) — ORM
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) — миграции
- [Redis](https://redis.io/) — Хранилище состояний
- [Fluent / fluentogram](https://projectfluent.org/) — Локализации
- [Dynaconf](https://www.dynaconf.com/) — Конфигурация приложения
- [structlog](https://www.structlog.org/en/stable/) — Логирования

---

## Запуск

1. Клонируйте репозиторий и перейдите в корень проекта.

2. Установите зависимости:

```bash
poetry install
```

3. Создайте файл конфигурации .secrets.toml:

```toml
[bot]
token = "TELEGRAM_BOT_TOKEN"

[db]
dsn = "postgresql+psycopg://superuser:superpassword@localhost:5432/data"

[redis]
dsn = "redis://localhost:6379"
```

4. Запустите контейнеры БД и Redis:

```bash
docker compose up -d
```

5. Примените миграции Alembic:

```bash
poetry run alembic upgrade head
```

6. Запустите приложение (бота):

```bash
poetry run python app.py
```

## Локализация

В проекте предусмотрена поддержка i18n (каталог `locales/`). При добавлении переводов регенерируйте бинарные `.mo` если используете gettext-пайплайн.


## Логирование

Проект использует structlog. Конфигурация и точка старта логов в `logs.startup`.