import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv


load_dotenv()


class EmailService:

    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def send_email(self, recipient: str, subject: str, body: str):

        msg = EmailMessage()
        msg["From"] = self.email
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.email, self.password)
            server.send_message(msg)

smtp_server =os.getenv("SMTP_SERVER")
smtp_port =os.getenv("SMTP_PORT")
email =os.getenv("EMAIL")
password =os.getenv('GAPP_PASSWORD')
email_service = EmailService(smtp_server, smtp_port, email, password)