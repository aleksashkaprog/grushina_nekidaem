# задаем базовый образ
FROM python:3.9

# устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# устанавливаем рабочую директорию
WORKDIR /code

# устанавливаем зависимости проекта
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# копируем проект в контейнер
COPY . /code/

# устанавливаем переменные окружения для PostgreSQL, Celery и Redis
ENV POSTGRES_DB=$DATABASE_NAME
ENV POSTGRES_USER=$DATABASE_USER
ENV POSTGRES_PASSWORD=$DATABASE_PASSWORD
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
ENV CELERY_BROKER_URL=redis://redis:6379/0
ENV CELERY_RESULT_BACKEND=redis://redis:6379/0

# ждем запуска базы данных PostgreSQL
# в случае использования официального образа postgres, может потребоваться установка postgresql-client
RUN apt-get update && apt-get install -y postgresql-client

# запускаем Celery worker и beat
CMD celery -A blog_api worker --concurrency=4 -l info -Ofair && celery -A myproject beat -l info

# для запуска веб-сервера Django, нужно раскомментировать следующую строку
# CMD python manage.py runserver 0.0.0.0:8000