from flask import Flask, request, jsonify
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import os

settings.configure(
    DEBUG=True,
    # Email settings
    EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    EMAIL_HOST='smtp.gmail.com',
    EMAIL_PORT=587,
    EMAIL_USE_TLS=True,
    EMAIL_HOST_USER='portal@thearkjuniorschool.com',
    EMAIL_HOST_PASSWORD='ioqm iivv yatz mbep\n',
    DEFAULT_FROM_EMAIL='portal@thearkjuniorschool.com',
    SERVER_EMAIL='portal@thearkjuniorschool.com',
    # Add any other required settings here
)

app = Flask(__name__)

@app.route("/")
def main_():
    return "Flask is running"

    
@app.route("/test/", methods=["GET"])
def test():
    return jsonify({"message": "API is working just fine"})

@app.route("/send_email/", methods=["GET"])
def send_email():
    data = request.get_json()
    message = EmailMultiAlternatives(
    to=[data["recipient"]],
        from_email="portal@thearkjuniorschool.com",
        subject=data["subject"],
    )
    template = data['template']
    template_path = f"/home/AtongJona2/email_api/email_templates/{template}.html"
    with open(template_path, "r", encoding="utf-8") as file:
        template_string = file.read()
    if template == "invite":
        template_string = template_string.replace("{{ user }}", data["user"])
    elif template == "forgot":
        url = f"https://{data['url']}"
        template_string = template_string.replace("{{ link }}", url)



    message.attach_alternative(template_string, "text/html")
    try:
        message.send(fail_silently=False)
        return jsonify({"message": "Success"})
    except Exception as e:
        return jsonify({"message": "Fail"})

if __name__ == "__main__":
    app.run(debug=True)
