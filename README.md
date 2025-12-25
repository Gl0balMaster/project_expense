# Expense Tracker
Expense Tracker — это веб-приложение на Django для отслеживания личных расходов с интуитивно понятным интерфейсом и полным набором функций для управления финансами. Пользователи могут добавлять расходы, просматривать историю, анализировать статистику и управлять своими финансовыми привычками через веб-интерфейс.
# Возможности проекта
Основные функции:
- Полная аутентификация — регистрация, вход, выход, сброс пароля
- Управление расходами — CRUD операции (создание, чтение, обновление, удаление)
- Статистика в реальном времени — общая сумма, расходы за сегодня/месяц, количество записей
- Фильтрация и сортировка — просмотр расходов по дате, пользователю
- Административная панель — полный контроль через Django Admin
# Технологии
- Backend: Python 3.10, Django 5.2
- Frontend: HTML5, CSS3, Bootstrap 5, JavaScript
- База данных: SQLite (разработка), PostgreSQL (продакшен через Docker)
- Тестирование: pytest, pytest-django, factory-boy, pytest-cov (Для запуска всех тестов в терминале пишем: pytest)
- Контейнеризация: Docker, Docker Compose
# Установка и запуск 
- Клонирование репозитории:
git clone https://github.com/Gl0balMaster/project_expense

- Установка и запуск проекта локально
Вариант 1: Без Docker 
1. Установить необходимые библиотеки:
pip install -r requirements.txt
2. Перейти в папку и создать миграции:
python.exe manage.py makemigrations
3. Активировать миграцию:
python.exe manage.py migrate
4. Запустить сервер:
python.exe manage.py runserver
Перейти по ссылке: 127.0.0.1:8000

Варинт 2: С Docker
1. Убедитесь что Docker Desktop запущен
2. Сборка и запуск контейнеров:
docker-compose up --build
3. При первом запуске выполните миграции:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
4. Открыть в браузере:
Приложение: http://localhost:8000
Админка: http://localhost:8000/admin

- Для создания суперпользователя:
python.exe manage.py createsuperuser
# Структура проекта
```text
project_expense/
├── .idea/                     # Конфигурационные файлы IDEs
├── expense_tracker/           # Основное приложение для отслеживания расходов
├── expenses/                  # Дополнительное приложение для расходов
├── users/                     # Приложение для управления пользователями
│
├── .coverage                  # Отчёты о покрытии кода тестами
├── .gitignore                 # Исключения для Git
├── db.sqlite3                 # База данных SQLite
├── docker-compose.yml         # Конфигурация Docker Compose
├── Dockerfile                 # Docker-образ приложения
├── manage.py                  # Django-скрипт управления проектом
├── .pytest.ini                # Конфигурация pytest
├── README.md                  # Документация проекта
├── requirements.txt           # Зависимости Python
└── settings.py                # Настройки Django