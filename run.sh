echo "Запуск Docker (backend + DB)"

if [ ! -f .requirements_hash ] || [ "$(sha256sum src/app/backend/requirements.txt)" != "$(cat .requirements_hash)" ]; then
    echo "requirements.txt изменился, пересобираем образ"
    docker compose down
    docker compose up --build -d
    sha256sum src/app/backend/requirements.txt > .requirements_hash
else
    echo "requirements.txt не изменился, используем существующие образы"
    docker compose up -d
fi

echo "Docker-контейнеры запущены"

echo "Запуск Electron + Vue"
cd src

pkill -f "vite" || true

npm run dev:frontend &
sleep 5
npm run dev:electron

echo "Все запущено успешно!"