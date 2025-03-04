# Djnago_rest_api

Краткое описание проекта. "Это API для управления пользователями, курсами и уроками в приложении".

## Содержание

- [Установка](#установка)
- [Docker](#docker)
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

## Celery

В этом проекте реализована функциональность для отправки уведомлений пользователям и управления их активностью с использованием Celery и Google SMTP сервера.

## Функциональность

### 1. Отправка уведомлений о курсе

Теперь, когда курс обновляется, пользователи, подписанные на этот курс, получают уведомление на свою электронную почту. Для отправки сообщений используется Google SMTP сервер, что обеспечивает надежную и безопасную доставку писем.

### 2. Проверка активности пользователей

С помощью Celery Beat настроена фоновая задача, которая проверяет активность пользователей каждые 24 часа. Если пользователь не заходил в систему более месяца, он автоматически блокируется. Это помогает поддерживать актуальность пользовательской базы и повышает безопасность системы.

## Установка и настройка

1. Убедитесь, что у вас установлен Celery и необходимые зависимости.
2. Настройте SMTP сервер в файле конфигурации вашего проекта для отправки почты.
3. Запустите Celery worker и Celery Beat в отдельных терминалах:

   ```bash
   # Запуск worker
   celery -A config worker --loglevel=info

   # Запуск beat
   celery -A config beat --loglevel=info
   ```
   
## Docker

### Шаги для запуска

1. Убедитесь, что у вас установлен Docker
2. Скопируйте файл `.env.example` в `.env` и заполните его вашими данными.
3. В корне проекта выполните команду:

   ```bash
   docker-compose up -d --build
   ```
4. После успешного запуска вы сможете проверить работоспособность сервисов:

Бэкенд: Перейдите по адресу http://localhost:8000
PostgreSQL: Подключитесь к базе данных на localhost:5432 с использованием указанных в .env данных.
Redis: Используйте redis-cli для подключения к localhost:6379.
Celery и Celery Beat: Логи можно просмотреть через docker-compose logs или подключившись к контейнерам.
### Остановка проекта
Чтобы остановить проект, выполните:
```bash
docker-compose down
````
## Использование
Приложение предоставляет API для управления пользователями, курсами и уроками. Вы можете создавать, обновлять, получать и удалять пользователей, курсы и уроки.

## Аутентификация
Для получения токена вам нужно отправить POST запрос на следующие эндпоинты:
1. Получение токена:

- URL: /api/token/
- Метод: POST
- Тело запроса (JSON):
```bash
{
    "username": "ваш_логин",
    "password": "ваш_пароль"
}
```
2. Обновление токена:

- URL: /api/token/refresh/
- Метод: POST
- Тело запроса (JSON):
```bash
{
    "refresh": "ваш_refresh_токен"
}
```
3. После получения токена, при отправке запросов добавьте заголовок:
```bash
Authorization: Bearer <token>
```

## Фикстуры
Фикстура для групп модераторов 
```bash
python manage.py loaddata users/fixtures/groups.json. 
```
Группа модераторов может просматривать все уроки и курсы, но без возможности создавать и удалять их. 
Обычные пользователи могут создавать, изменять и удалять только свои курсы и уроки.
## Эндпоинты

### Пользователи
- POST /users/profile/ - Создание нового пользователя
- GET /users/profile/{id}/ - Получение информации о пользователе
- PUT /users/profile/{id}/ - Обновление информации о пользователе
- DELETE /users/profile/{id}/ - Удаление пользователя
### Платежи
- POST /users/payments/ - Создание нового платежа
- GET /users/payments/{id}/ - Получение информации о платеже
- PUT /users/payments/{id}/ - Обновление информации о платеже
- DELETE /users/payments/{id}/ - Удаление платежа
### Кастомная команда для заполнения платежей
```bash
python manage.py populate_payments
```
### Фильтрация и сортировка
Добавлены возможности фильтрации и сортировки для платежей:
- paid_course - сортировка по курсу
- paid_lesson - сортировка по уроку
- payment_method - сортировка по методу платежа
### Пример запроса сортировки
- Метод: GET
- URL: http://localhost:8000/users/payments/?paid_course=1&payment_method=cash
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
### Вложенность
- Курсы 
Теперь, когда вы делаете запрос к курсу, также выводятся вложенные уроки. 
Это позволяет вам получать всю необходимую информацию о курсе и связанных с ним уроках в одном запросе.
- Пользователи
Теперь в профиле пользователя также отображаются вложенные платежи. 
- Это позволяет получить информацию о платежах, связанных с конкретным пользователем, в одном запросе.
## Примеры запросов в Postman
1. Создание нового пользователя
- Метод: POST
- URL: http://localhost:8000/users/profile/
- Тело запроса (формат JSON):
```bash
{
    "email": "user@example.com",
    "phone": "+1234567890",
    "city": "CityName",
    "password": "your_password"
}
```
2. Создание нового курса
- Метод: POST
URL: http://localhost:8000/api/courses/
- Тело запроса (формат JSON):
```bash
{
    "title": "Название курса",
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
