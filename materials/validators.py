# materials/validators.py
from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def validate_video_link(value):
    """
    Разрешаем только ссылки на youtube.com (включая youtu.be).
    Бросаем ValidationError для всех остальных доменов.
    """
    if not value:
        return

    parsed = urlparse(value)
    hostname = parsed.hostname or ""
    hostname = hostname.lower()

    allowed = ("youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com")
    if hostname not in allowed:
        raise ValidationError("Разрешены только ссылки на YouTube (youtube.com / youtu.be).")
