from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv("config.env")
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

app = Flask(__name__)

class EmailRequest:
    def __init__(self, recipient_email, subject, body):
        self.recipient_email = recipient_email
        self.subject = subject
        self.body = body
@app.route("/")
def main_():
    return "Flask is running"

    
@app.route("/test/", methods=["GET"])
def test():
    return jsonify({"message": "API is working just fine"})

@app.route("/send_email/", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        email_request = EmailRequest(
            recipient_email=data["recipient_email"],
            subject=data["subject"],
            body=data["body"]
        )

        # Create the email message
        msg = MIMEText(email_request.body)
        msg["Subject"] = email_request.subject
        msg["From"] = EMAIL
        msg["To"] = email_request.recipient_email

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.ehlo()
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(EMAIL, email_request.recipient_email, msg.as_string())

        return jsonify({"message": "Email sent successfully!"})

    except Exception as e:
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
