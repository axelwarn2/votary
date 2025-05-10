from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import EmployeeRoute, MeetingRoute, TaskRoute, RecordRoute

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(EmployeeRoute.router)
app.include_router(MeetingRoute.router)
app.include_router(TaskRoute.router)
app.include_router(RecordRoute.router)
