FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    ffmpeg \
    libopenblas-dev \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./src/app/backend/requirements.txt /app/backend/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r backend/requirements.txt && rm -rf /var/lib/apt/lists/*

COPY ./src/app/ /app

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]