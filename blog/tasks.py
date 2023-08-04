from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


@shared_task
def post_email(subject, message, email):
    """Sending email after creating post or comment"""
    mail_sent = send_mail(
        subject,
        message,
        settings.NOREPLY_EMAIL,
        [email],
        fail_silently=False,
    )
    return mail_sent
