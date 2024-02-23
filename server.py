from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


load_dotenv("config.env")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

app = FastAPI()

class EmailRequest(BaseModel):
    recipient_email: str
    subject: str
    body: str


@app.get("/test/")
async def test():
    return {"message": "API is working"}

@app.get("/send_email/")
async def send_email(email_request: EmailRequest):
    try:
        # Create the email message
        sender_email = "portal@thearkjuniorschool.com"
        msg = MIMEText(email_request.body)
        msg["Subject"] = email_request.subject
        msg["From"] = sender_email
        msg["To"] = email_request.recipient_email

        # Send the email

        # Close the connection
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.ehlo()
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(sender_email, email_request.recipient_email, msg.as_string())

        return {"message": "Email sent successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
