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

COPY ./src/app/backend/requirements.txt /app/backend/requirements.txt

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip && pip install --no-cache-dir -r backend/requirements.txt

# Копируем остальной код
COPY ./src/app/ /app

# Команда запуска FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]