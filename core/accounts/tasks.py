from celery import shared_task
from mail_templated import EmailMessage
from core.settings import SITE_DOMAIN


@shared_task
def send_verify_email(token, email):
    message = EmailMessage(
        "email/email-verify.tpl",
        {"token": token, "site_domain": SITE_DOMAIN},
        "test@test.com",
        to=[email],
    )
    message.send()


@shared_task
def send_reset_password_email(token, uidb64, email):
    message = EmailMessage(
        "email/forget-password.tpl",
        {"token": token, "uidb64": uidb64, "site_domain": SITE_DOMAIN},
        "test@test.com",
        to=[email],
    )
    message.send()
