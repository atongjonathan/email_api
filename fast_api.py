from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
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
        msg = MIMEMultipart("alternative")
        msg["Subject"] = email_request.subject
        msg["From"] = EMAIL
        msg["To"] = email_request.recipient_email

        # Send the email
        text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
        html = """\
        <html>
        <head></head>
        <body>
            <p>Hi!<br>
            How are you?<br>
            Here is the <a href="http://www.python.org">link</a> you wanted.
            </p>
        </body>
        </html>
        """
        # Close the connection
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.ehlo()
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(EMAIL, email_request.recipient_email, msg.as_string())

        return {"message": "Email sent successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
