from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(subject, message, sender, recipients):
    send_mail(subject, message, sender, recipients, fail_silently=False)
