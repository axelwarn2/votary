# fastapi/Dockerfile

FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y gcc libpq-dev

# Установка зависимостей проекта
WORKDIR /app

COPY ./src/app/backend /app
COPY ./src/app/backend/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

# Экспонируем порт
EXPOSE 8000

# Команда запуска FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
