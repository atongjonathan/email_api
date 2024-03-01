from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import os
password = os.environ.get("APP_PASSWORD") + "\n"
def send_my_email():
    settings.configure(
        DEBUG = True,
        EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend",
        EMAIL_HOST = 'smtp.gmail.com',
        EMAIL_PORT = 587,
        EMAIL_USE_TLS = True,
        EMAIL_HOST_USER = "atongjonathan@gmail.com",
        EMAIL_HOST_PASSWORD = password,

    )

    email = EmailMultiAlternatives(
        to=["atongjonathan2@gmail.com"],from_email="atongjonathan@gmail.com", subject="Testnng Inline CSS"
    )
    with open("html.text", encoding="utf-8") as file:
        email_text = file.read()
    email.attach_alternative(email_text, "text/html")
    email.send(fail_silently=False)

send_my_email()