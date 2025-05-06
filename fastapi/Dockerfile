FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    ffmpeg \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование исходного кода
COPY ./src/app/ /app

# Установка зависимостей Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r backend/requirements.txt

# Экспонируем порт
EXPOSE 8000

# Команда запуска FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]