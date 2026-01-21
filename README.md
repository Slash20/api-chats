# Chat API

Тестовое задание: API для чатов и сообщений.

Проект реализован на FastAPI, использует PostgreSQL, SQLAlchemy, Alembic, полностью обёрнут в Docker / docker-compose.

---

## Функциональность

### Модели

* Chat

  * id: int
  * title: str (1–200, не пустой)
  * created_at: datetime

* Message

  * id: int
  * chat_id: int (FK → Chat)
  * text: str (1–5000, не пустой)
  * created_at: datetime

Связь один ко многим

---

### API эндпоинты

#### 1. Создать чат

POST /chats/

{
  "title": "My chat"
}

В качестве ответа возвращает данные о созданном чате.

---

#### 2. Отправить сообщение

POST /chats/{id}/messages/

{
  "text": "Hi"
}
* Возвращает 404, если чат не существует

---

#### 3. Получить чат и последние сообщения

GET /chats/{id}

* limit: по умолчанию 20, максимум 100
* Возвращает сообщения, отсортированные по created_at

---

#### 4. Удалить чат

DELETE /chats/{id}

* удаляет чат и все сообщения каскадно
* В качестве ответа возвращает 204 No Content

---

## Технологии

* Python 3.11
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Docker / docker-compose
* Pydantic

---

## Запуск проекта через Docker

### 1. Собрать и запустить контейнеры
### Предварительно должен быть запущен Docker Desktop

```shell
docker compose up -d --build
```
Проверить статус:

```shell
docker compose ps
```
---

### 2. Применить миграции

```shell
docker compose exec api alembic upgrade head
```
---

### 3. Открыть API

* Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

### Примечание: если нужно посмотреть данные в базе данных в рамках Docker, то нужно запустить следующие команды (делается после проведения миграций):

### 1. Заходим в базу данных в рамках Docker:
```shell
docker compose exec db psql -U postgres -d chat_db
```

### 2. Когда зашли в базу данных, смотрим, что в ней хранится:

Чаты
```sql
select * from chats;
```

Сообщения
```sql
select * from messages;
```

