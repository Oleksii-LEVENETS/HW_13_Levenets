import datetime

from celery import shared_task

from django.core.mail import send_mail


# Create your tasks here


@shared_task
def reminder_task(email, reminder_text):
    send_mail(
        f"Reminder. Now is: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"{reminder_text}",
        "admin@noreply.com",
        [email],
        fail_silently=False,
    )
    return
