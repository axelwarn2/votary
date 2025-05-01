from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import EmployeeRoute, MeetingRoute, TaskRoute

app = FastAPI()

# Разрешаем CORS, чтобы frontend мог отправлять запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(EmployeeRoute.router)
app.include_router(MeetingRoute.router)
app.include_router(TaskRoute.router)
