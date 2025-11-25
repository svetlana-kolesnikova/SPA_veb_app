# users/tasks.py
from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def deactivate_inactive_users():
    """
    Периодическая задача по блокировке неактивных пользователей
    """

    threshold = timezone.now() - timedelta(days=30)
    users = User.objects.filter(last_login__lt=threshold, is_active=True)
    for user in users:
        user.is_active = False
        user.save()
