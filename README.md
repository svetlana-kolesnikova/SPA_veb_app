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

| Приложение  | Назначение                    |
| ----------- | ----------------------------- |
| `users`     | кастомная модель пользователя |
| `materials` | модели курсов и уроков, API   |


## Модели проекта

###  Пользователь (users.User)

- email (используется вместо логина)

- phone

- city

- avatar

Авторизация проходит по email, username отключён.


### Course (Курс)

- name

- preview (изображение)

- description

### Lesson (Урок)

- name

- description

- preview

- video_link

- course — связь с Course (один курс → много уроков)

---

## API Эндпоинтыv

### Курсы — ViewSet
| Метод     | URL                  | Описание      |
| --------- |----------------------| ------------- |
| GET       | `/api/courses/`      | список курсов |
| POST      | `/api/courses/`      | создать курс  |
| GET       | `/api/courses/<id>/` | получить курс |
| PUT/PATCH | `/api/courses/<id>/` | обновить курс |
| DELETE    | `/api/courses/<id>/` | удалить курс  |


### Уроки — Generic Views
| Метод     | URL                  | Описание      |
| --------- | -------------------- | ------------- |
| GET       | `/api/lessons/`      | список уроков |
| POST      | `/api/lessons/`      | создать урок  |
| GET       | `/api/lessons/<id>/` | получить урок |
| PUT/PATCH | `/api/lessons/<id>/` | изменить урок |
| DELETE    | `/api/lessons/<id>/` | удалить урок  |

### Пользователи — ViewSet
| Метод     | URL                | Описание              |
| --------- | ------------------ | --------------------- |
| GET       | `/api/users/`      | список пользователей  |
| POST      | `/api/users/`      | создать пользователя  |
| GET       | `/api/users/<id>/` | получить пользователя |
| PUT/PATCH | `/api/users/<id>/` | изменить              |
| DELETE    | `/api/users/<id>/` | удалить               |


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