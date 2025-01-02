# Djnago_rest_api

Краткое описание вашего проекта. Например, "Это API для управления пользователями, курсами и уроками в приложении".

## Содержание

- [Установка](#установка)
- [Использование](#использование)
- [Примеры запросов в Postman](#примеры-запросов-в-postman)

## Установка

1. Клонируйте репозиторий:

```bash
   git clone https://github.com/ваш-логин/ваш-репозиторий.git
   cd ваш-репозиторий
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:

```bash
pip install -r req.txt
```

4. Примените миграции:

```bash
python manage.py migrate
```

5. Запустите сервер:
```bash
python manage.py runserver
```

Теперь ваше приложение доступно по адресу http://localhost:8000/.

## Использование
Приложение предоставляет API для управления пользователями, курсами и уроками. Вы можете создавать, обновлять, получать и удалять пользователей, курсы и уроки.

## Эндпоинты

### Пользователи
- POST /users/profile/ - Создание нового пользователя
- GET /users/profile/{id}/ - Получение информации о пользователе
- PUT /users/profile/{id}/ - Обновление информации о пользователе
- DELETE /users/profile/{id}/ - Удаление пользователя
### Курсы
- POST /api/courses/ - Создание нового курса
- GET /api/courses/{id}/ - Получение информации о курсе
- PUT /api/courses/{id}/ - Обновление информации о курсе
- DELETE /api/courses/{id}/ - Удаление курса
- GET /api/courses/ - Получение списка всех курсов
### Уроки
- POST /api/lessons/ - Создание нового урока
- GET /api/lessons/{id}/ - Получение информации об уроке
- PUT /api/lessons/{id}/ - Обновление информации об уроке
- DELETE /api/lessons/{id}/ - Удаление урока
- GET /api/courses/{course_id}/lessons/ - Получение списка всех уроков для конкретного курса
## Примеры запросов в Postman
1. Создание нового пользователя
- Метод: POST
- URL: http://localhost:8000/users/profile/
- Тело запроса (формат JSON):
```bash
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "strongpassword",
    "first_name": "Имя",
    "last_name": "Фамилия"
}
```
2. Создание нового курса
- Метод: POST
URL: http://localhost:8000/api/courses/
- Тело запроса (формат JSON):
```bash
{
    "title": "Название курса",
    "preview_image": "URL_картинки_предпросмотра",
    "description": "Описание курса"
}
```
3. Получение информации о курсе
- Метод: GET
- URL: http://localhost:8000/api/courses/1/ (где 1 - это ID курса)
4. Создание нового урока
- Метод: POST
- URL: http://localhost:8000/api/lessons/
- Тело запроса (формат JSON):
```bash
{
    "title": "Название урока",
    "description": "Описание урока",
    "preview_image": "URL_картинки_предпросмотра",
    "video_link": "https://link_на_видео",
    "course": 1  # ID курса, к которому относится урок
}
```
5. Получение информации об уроке
- Метод: GET
- URL: http://localhost:8000/api/lessons/1/ (где 1 - это ID урока)
6. Удаление курса
- Метод: DELETE
- URL: http://localhost:8000/api/courses/1/ (где 1 - это ID курса)
7. Удаление урока
- Метод: DELETE
- URL: http://localhost:8000/api/lessons/1/ (где 1 - это ID урока)