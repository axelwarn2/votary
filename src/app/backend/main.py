# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import employee

app = FastAPI()

# Разрешаем CORS, чтобы frontend мог отправлять запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно ограничить до http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee.router)