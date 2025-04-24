#!/bin/bash

echo "Запуск Docker (backend + DB)"
docker compose up --build -d

echo "Docker-контейнеры запущены"

echo "Запуск Electron + Vue"
cd src && npm run dev

echo "Все запущено успешно!"