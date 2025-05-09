import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime
import os
from backend.repositories.EmployeeRepository import EmployeeRepository
from sqlalchemy.orm import Session

class EmailService:
    def __init__(self, db: Session):
        self.db = db
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")

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
        