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

### 3. Применить миграции
```bash
python manage.py migrate
```

### 4. Создать суперпользователя (опционально)
```bash
python manage.py createsuperuser
```

### 5. Запустить сервер
```bash
python manage.py runserver
```

---

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

---

## API Эндпоинтыv

### Курсы — ViewSet
| Метод     | URL                  | Описание                                |
| --------- | -------------------- | --------------------------------------- |
| GET       | `/api/courses/`      | список курсов (с количеством и уроками) |
| POST      | `/api/courses/`      | создать курс                            |
| GET       | `/api/courses/<id>/` | получить курс                           |
| PUT/PATCH | `/api/courses/<id>/` | обновить курс                           |
| DELETE    | `/api/courses/<id>/` | удалить курс                            |


### Уроки — Generic Views
| Метод     | URL                  | Описание      |
| --------- | -------------------- | ------------- |
| GET       | `/api/lessons/`      | список уроков |
| POST      | `/api/lessons/`      | создать урок  |
| GET       | `/api/lessons/<id>/` | получить урок |
| PUT/PATCH | `/api/lessons/<id>/` | изменить урок |
| DELETE    | `/api/lessons/<id>/` | удалить урок  |


### Пользователи — ViewSet
| Метод     | URL                | Описание                                  |
| --------- | ------------------ | ----------------------------------------- |
| GET       | `/api/users/`      | список пользователей                      |
| POST      | `/api/users/`      | создать пользователя                      |
| GET       | `/api/users/<id>/` | получить пользователя с историей платежей |
| PUT/PATCH | `/api/users/<id>/` | изменить данные                           |
| DELETE    | `/api/users/<id>/` | удалить пользователя                      |



### Платежи (ViewSet + фильтрация)
| Метод     | URL                   | Описание        |
| --------- | --------------------- | --------------- |
| GET       | `/api/payments/`      | список платежей |
| POST      | `/api/payments/`      | создать запись  |
| GET       | `/api/payments/<id>/` | получить запись |
| PUT/PATCH | `/api/payments/<id>/` | изменить        |
| DELETE    | `/api/payments/<id>/` | удалить         |


### Пример фикстуры платежей [payments.json](users%2Ffixtures%2Fpayments.json)

___

## Требования

Файл pyproject.toml должен включать:
```bash
[tool.poetry.dependencies]
python = "^3.11"
django = "^5.0"
djangorestframework = "^3.15"
pillow = "^10.0"
```

___
### Автор
Svetlana Kolesnikova