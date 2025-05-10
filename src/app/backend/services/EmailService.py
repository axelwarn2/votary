import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime
import os
import logging
from backend.repositories.EmployeeRepository import EmployeeRepository
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, db: Session):
        self.db = db
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.base_url = os.getenv("BASE_URL", "http://localhost:8000")
       
    def send_task_email(self, task_description: str, employee_id: int, leader_id: int, task_created: datetime):
        employee_repo = EmployeeRepository(self.db)
        employee = employee_repo.get_employee_by_id(employee_id)
        leader = employee_repo.get_employee_by_id(leader_id)

        if not employee or not leader:
            raise ValueError("Employee or leader not found")
        
        employee_email = employee["email"]
        leader_email = leader["email"]
        leader_name = f"{leader['surname']} {leader['name']}"

        subject = f"Задача от {task_created.strftime('%Y-%m-%d %H:%M:%S')}"

        body = (
            f"Уважаемый(ая) {employee['surname']} {employee['name']}, Вам поставлена новая задача:\n\n"
            f"{task_description}\n\n"
            f"Поставил задачу: {leader_name}\n"
            f"Срок выполнения: {task_created:%Y-%m-%d %H:%M:%S}\n\n"
            f"С уважением,\n"
            f"{leader_name}"
        )

        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = f"{leader_name} <{leader_email}>"
        msg["To"] = employee_email
        msg["Reply-To"] = leader_email

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, employee_email, msg.as_string())
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}")
        
    def send_reminder_email(self, task_id: int, task_description: str, employee_id: int, leader_id: int, deadline: datetime):
        logger.info(f"Sending reminder email for task_id: {task_id}, employee_id: {employee_id}")
        employee_repo = EmployeeRepository(self.db)
        employee = employee_repo.get_employee_by_id(employee_id)
        leader = employee_repo.get_employee_by_id(leader_id)

        if not employee or not leader:
            logger.error(f"Employee or leader not found: employee_id={employee_id}, leader_id={leader_id}")
            raise ValueError("Employee or leader not found")

        employee_email = employee["email"]
        leader_email = leader["email"]
        leader_name = f"{leader['surname']} {leader['name']}"
        logger.info(f"Reminder email: employee_email={employee_email}, leader_email={leader_email}")

        complete_url = f"{self.base_url}/tasks/{task_id}/complete"
        logger.info(f"Complete URL: {complete_url}")

        subject = "Напоминание: Завершите задачу сегодня"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h3>Уважаемый(ая) {employee['surname']} {employee['name']},</h3>
            <p>Напоминаем, что сегодня истекает срок выполнения задачи:</p>
            <p><strong>{task_description}</strong></p>
            <p>Поставил задачу: {leader_name}</p>
            <p>Срок выполнения: {deadline.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>
                <a href="{complete_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                    Завершить задачу
                </a>
            </p>
            <p>С уважением,<br>{leader_name}</p>
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg.attach(MIMEText(html_body, "html", "utf-8"))
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = f"{leader_name} <{leader_email}>"
        msg["To"] = employee_email
        msg["Reply-To"] = leader_email

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, employee_email, msg.as_string())
                logger.info(f"Reminder email sent to {employee_email} for task_id: {task_id}")
        except Exception as e:
            logger.error(f"Failed to send reminder email to {employee_email} for task_id: {task_id}: {str(e)}")
            raise RuntimeError(f"Failed to send email: {str(e)}")
        