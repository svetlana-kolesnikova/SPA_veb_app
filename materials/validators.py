# materials/validators.py
from urllib.parse import urlparse
from rest_framework.serializers import ValidationError


class VideoLinkValidator:
    """
    Класс-валидатор для поля ссылки на видео.
    """

    def __init__(self, field: str = "video_link"):
        self.field = field
        self.__fields__ = [field]

    def __call__(self, attrs):
        """
        Вызов валидатора.
        """

        value = attrs.get(self.field) if isinstance(attrs, dict) else attrs

        if not value:
            return attrs  # ничего не валидируем, пустая ссылка допустима

        parsed = urlparse(value)
        hostname = (parsed.hostname or "").lower()

        allowed = (
            "youtube.com",
            "www.youtube.com",
            "youtu.be",
            "m.youtube.com",
            "music.youtube.com",
        )

        if hostname not in allowed:
            raise ValidationError({self.field: "Разрешены только ссылки на YouTube (youtube.com / youtu.be)."})

        return attrs

