from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import EmployeeRoute, MeetingRoute, TaskRoute, RecordRoute
from backend.repositories.TaskRepository import TaskRepository
from backend.services.EmailService import EmailService
from backend.utlis.db import get_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import asyncio

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def start_scheduler():
    logger.info("Starting scheduler initialization")
    try:
        async def send_reminders():
            try:
                db = next(get_db())
                task_repo = TaskRepository(db)
                email_service = EmailService(db)
                tasks = task_repo.get_tasks_due_tomorrow()
                logger.info(f"Found {len(tasks)} tasks due tomorrow: {[{'id': task['id'], 'status': task['status']} for task in tasks]}")
                for task in tasks:
                    try:
                        email_service.send_reminder_email(
                            task_id=task["id"],
                            task_description=task["description"],
                            employee_id=task["employee_id"],
                            leader_id=task["leader_id"],
                            deadline=task["deadline"]
                        )
                        logger.info(f"Sent reminder email for task ID {task['id']} to employee ID {task['employee_id']}")
                    except Exception as e:
                        logger.error(f"Failed to send reminder email for task ID {task['id']}: {str(e)}")
            except Exception as e:
                logger.error(f"Error in send_reminders: {str(e)}")
                raise

        scheduler.add_job(
            send_reminders,
            trigger=CronTrigger(minute="*/1"),
            id="send_reminders",
            replace_existing=True
        )
        scheduler.start()
        logger.info("Scheduler started")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {str(e)}")
        raise

@app.on_event("startup")
async def startup_event():
    logger.info("Startup event triggered")
    asyncio.create_task(start_scheduler())

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutdown event triggered")
    scheduler.shutdown()
    logger.info("Scheduler shutdown")
