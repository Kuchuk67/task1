
# Указываем базовый образ
FROM python:3.12
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
RUN pip install poetry
COPY ./backend/pyproject.toml ./
RUN poetry install --no-root

COPY ./backend .

COPY ./backend/docker/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./backend/docker/celery/worker/start /start_celeryworker
RUN sed -i 's/\r$//g' /start_celeryworker
RUN chmod +x /start_celeryworker

COPY ./backend/docker/celery/beat/start /start_celerybeat
RUN sed -i 's/\r$//g' /start_celerybeat
RUN chmod +x /start_celerybeat

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]