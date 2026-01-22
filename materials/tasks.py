# materials/tasks.py
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_course_update_email(user_email: str, course_name: str):
    """
    Задача по асинхронной рассылке писем при обновлении курса
    """
    send_mail(
        subject=f"Обновление курса: {course_name}",
        message=f"Курс {course_name} был обновлён. Заходите и изучайте новые материалы!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
    )
