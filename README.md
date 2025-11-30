# DRF Courses API

Учебный проект на Django + Django REST Framework.  
Проект реализует модели пользователей, курсов и уроков, а также предоставляет REST API для их управления.

---

## Стек технологий

- Python 3.11+
- Poetry
- Django 5
- Django REST Framework
- Pillow (для загрузки изображений)
- SQLite / PostgreSQL (на выбор)
- Celery + Redis (асинхронные задачи)
- Stripe (оплата курсов и уроков)
- drf-yasg / drf-spectacular (Swagger / Redoc документация)
- djangorestframework-simplejwt (JWT авторизация)

---

## Установка и запуск проекта

### 1. Клонировать проект
```bash
git clone <ссылка на репозиторий>
cd drf_project
```

### 2. Установить зависимости через Poetry
```bash
poetry install
poetry shell
```
### 3. Настроить .env файл
Удалить из названия файла 
[.env_sample](.env_sample)    "_sample" 

### 4. Применить миграции
```bash
python manage.py migrate
```

### 5. Создать суперпользователя (опционально)
```bash
python manage.py createsuperuser
```

### 6. Запустить сервер
```bash
python manage.py runserver
```
___
## Docker

### Dockerfile
Файл Dockerfile находится в корне проекта и используется для сборки образов всех сервисов (web, celery, beat).


### Docker Compose
Файл [docker-compose.yaml](docker-compose.yaml) подключает все сервисы и переменные окружения из .env:
```bash
docker-compose up --build
```

### Сервисы после запуска:
| Сервис   | Описание                                 | Порт |
| -------- | ---------------------------------------- | ---- |
| `web`    | Django backend                           | 8000 |
| `db`     | PostgreSQL                               | 5432 |
| `redis`  | Redis для Celery                         | 6379 |
| `celery` | Worker Celery для асинхронных задач      | —    |
| `beat`   | Планировщик периодических задач (Celery) | —    |

___

## Приложения

| Приложение  | Назначение                             |
| ----------- |----------------------------------------|
| `users`     | кастомная модель пользователя и оплаты |
| `materials` | модели курсов и уроков, API            |


## Модели проекта

###  Пользователь (users.User)

- email (используется вместо логина)

- phone

- city

- avatar

Авторизация проходит по email, username отключён.


## Платеж (users.Payment)

- user — ссылка на пользователя

- payment_date — дата и время оплаты

- course — ссылка на оплаченный курс (опционально)

- lesson — ссылка на оплаченный урок (опционально)

- amount — сумма оплаты

- payment_method — способ оплаты (cash или transfer)

- Хранение Stripe-сессий и URL для оплаты


### Course (Курс)

- name

- preview (изображение)

- description

- lesson_count — автоматически вычисляемое количество уроков

- lessons — список связанных уроков (вложенный сериализатор)


### Lesson (Урок)

- name

- description

- preview

- video_link

- course — связь с Course (один курс → много уроков)

### Subscription (Подписка на курс)

- user — ссылка на пользователя

- course — ссылка на курс

- позволяет отслеживать, подписан ли пользователь на обновления курса

- используется для отправки уведомлений при обновлении курса


---

## API Эндпоинтыv

### Курсы — ViewSet
| Метод     | URL                                        | Описание                                                          |
| --------- | ------------------------------------------ | ----------------------------------------------------------------- |
| GET       | `/api/materials/courses/`                  | список курсов (с количеством и уроками, поддерживается пагинация) |
| POST      | `/api/materials/courses/`                  | создать курс                                                      |
| GET       | `/api/materials/courses/<id>/`             | получить курс                                                     |
| PUT/PATCH | `/api/materials/courses/<id>/`             | обновить курс                                                     |
| DELETE    | `/api/materials/courses/<id>/`             | удалить курс                                                      |
| POST      | `/api/materials/courses/<id>/subscribe/`   | подписаться на курс                                               |
| POST      | `/api/materials/courses/<id>/unsubscribe/` | отписаться от курса                                               |



### Уроки — Generic Views
| Метод     | URL                  | Описание                                 |
| --------- | -------------------- | ---------------------------------------- |
| GET       | `/api/lessons/`      | список уроков (с пагинацией)             |
| POST      | `/api/lessons/`      | создать урок (валидатор ссылок на видео) |
| GET       | `/api/lessons/<id>/` | получить урок                            |
| PUT/PATCH | `/api/lessons/<id>/` | изменить урок                            |
| DELETE    | `/api/lessons/<id>/` | удалить урок                             |


### Пользователи — ViewSet
| Метод     | URL                | Описание                                  |
| --------- | ------------------ | ----------------------------------------- |
| GET       | `/api/users/`      | список пользователей                      |
| POST      | `/api/users/`      | создать пользователя                      |
| GET       | `/api/users/<id>/` | получить пользователя с историей платежей |
| PUT/PATCH | `/api/users/<id>/` | изменить данные                           |
| DELETE    | `/api/users/<id>/` | удалить пользователя                      |


### Подписка на курс
| Метод  | URL                              | Описание                                                  |
| ------ | -------------------------------- | --------------------------------------------------------- |
| POST   | `/api/courses/<id>/subscribe/`   | подписаться на курс                                       |
| DELETE | `/api/courses/<id>/unsubscribe/` | отписаться от курса                                       |
| GET    | `/api/courses/<id>/`             | возвращает поле `is_subscribed` для текущего пользователя |


### Платежи (ViewSet + фильтрация)
| Метод     | URL                                        | Описание                       |
| --------- | ------------------------------------------ | ------------------------------ |
| GET       | `/api/users/payments/`                     | список платежей                |
| POST      | `/api/users/payments/buy/`                 | создать Stripe-платёж и сессию |
| GET       | `/api/users/payments/<id>/`                | получить запись                |
| PUT/PATCH | `/api/users/payments/<id>/`                | изменить                       |
| DELETE    | `/api/users/payments/<id>/`                | удалить                        |
| GET       | `/api/users/payments/status/<session_id>/` | получить статус Stripe-сессии  |



### Пример фикстуры платежей [payments.json](users%2Ffixtures%2Fpayments.json)

___

Для уроков и курсов используется класс пагинации [StandardResultsSetPagination](materials%2Fpaginators.py)

Валидация ссылок [validators.py](materials%2Fvalidators.py)

Тесты [tests.py](materials%2Ftests.py)

___
## Требования

Файл pyproject.toml должен включать:
```bash
[tool.poetry.dependencies]
"django (>=5.2.8,<6.0.0)",
"djangorestframework (>=3.16.1,<4.0.0)",
"pillow (>=12.0.0,<13.0.0)",
"dotenv (>=0.9.9,<0.10.0)",
"psycopg2 (>=2.9.11,<3.0.0)",
"django-filter (>=25.2,<26.0)",
"djangorestframework-simplejwt (>=5.5.1,<6.0.0)",
"ipython (>=9.7.0,<10.0.0)",
"pytest (>=9.0.1,<10.0.0)",
"pytest-django (>=4.11.1,<5.0.0)",
"coverage (>=7.11.3,<8.0.0)"
"drf-spectacular (>=0.29.0,<0.30.0)",
"drf-spectacular-sidecar (>=2025.10.1,<2026.0.0)",
"stripe (>=14.0.0,<15.0.0)",
"drf-yasg (>=1.21.11,<2.0.0)",
"celery (>=5.5.3,<6.0.0)",
"redis (>=7.1.0,<8.0.0)"
```

___
### Автор
Svetlana Kolesnikova