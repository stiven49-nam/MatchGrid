Структура проекта text matchgrid/ 
├── Dockerfile 
├── docker-compose.yml 
├── .env.example 
├── requirements.txt 
├── readmy.md 
├── manage.py 
├── matchgrid/ 
│ ├──init.py 
│ ├──settings.py 
│ ├──urls.py 
│ └── wsgi.py 
├──users/ 
│ ├──init.py 
│ ├──models.py 
│ ├──serializers.py 
│ ├──views.py 
│ ├──urls.py 
│ └──admin.py 
├──interactions/ 
│ ├──init.py 
│ ├──models.py 
│ ├──serializers.py 
│ ├──views.py 
│ ├──urls.py 
│ └──admin.py 
└── core/ 
├── init.py 
├── pagination.py 
└── utils.py

✅ Шаг 1. Создание проекта meetup bash django-admin startproject matchgrid cd matchgrid ✅ Шаг 2. Создание приложений bash mkdir apps\core cd apps python manage.py startapp users python manage.py startapp interactions

✅ Шаг 3. Регистрация приложений в файле settings.py

✅ Шаг 4. Модели данных

✅ Шаг 5. Регистрация моделей в админке

✅ Шаг 6. Создание миграций и запуск сервера bash python manage.py makemigrations python manage.py migrate python manage.py createsuperuser # Создайте суперпользователя для доступа к админке python manage.py runserver

Используйте виртуальное окружение перед созданием requirements.txt:

bash python -m venv venv исходный код venv/bin/активировать # Linux / macOS venv \ Скрипты \ активировать # Windows pip установить django pip заморозить > requirements.txt pip установка psycopg2 git clone https://github.com/your-username/meetup-app.git

Создайте файл .env на основе .env.example:

bash cp .env.example .env Запустите проект с помощью Docker Compose:

bash docker-compose up --build Применение миграций (выполняется автоматически при запуске):

bash docker-compose exec web python manage.py migrate Создание суперпользователя (необязательно):

bash docker-compose exec web python manage.py createsuperuser Доступ к API Основное API: http://localhost:8000/api/

Админ-панель: http://localhost:8000/admin/

Swagger документация: http://localhost:8000/swagger/

ReDoc документация: http://localhost:8000/redoc/

Основные эндпоинты Аутентификация POST /api/token/ - Получение JWT токена

POST /api/token/refresh/ - Обновление токена

Пользователи POST /api/users/register/ - Регистрация пользователя

GET /api/users/profile/ - Профиль текущего пользователя

GET /api/users/users/ - Список пользователей с фильтрацией

GET /api/users/random-profile/ - Случайный профиль

Взаимодействия POST /api/interactions/interact/ - Лайк/дизлайк/просмотр

GET /api/interactions/history/{action}/ - История действий

GET /api/interactions/likes-history/ - История лайков профиля

GET /api/interactions/matches/ - Список матчей

POST /api/interactions/invitations/ - Отправка приглашения

Фильтрация пользователей Доступные параметры фильтрации:

gender - пол (M/F/O)

city - город

статус - статус (ищу / занят / сложно / не ищу)

min_age - минимальный возраст

max_age - максимальный возраст

Пример:

text GET /api/users/users/?gender=F&city=Москва&min_age=20&max_age=30 Модели данных Пользователь Email (уникальный)

Пароль

Дата регистрации

Профиль пользователя ФИО

Пол

Возраст

Город

Увлечения

Статус

Количество лайков

Настройки приватности

Фотогалерея

Взаимодействия Лайки/дизлайки

Просмотры

Матчи (взаимные лайки)

Приглашения на свидания

Технологии Django 4.2

Django REST Framework 3.14

PostgreSQL

JWT аутентификация

Докер

Swagger/OpenAPI документация

текст
