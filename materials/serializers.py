# materials/serializers.py
from rest_framework import serializers

from .models import Course, Lesson
from .validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели Lesson"""

    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    video_link = serializers.URLField(required=False, allow_blank=True,)

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "preview", "video_link", "course", "owner"]
        validators = [VideoLinkValidator(field="video_link")]

    def create(self, validated_data):
        """
        Автоматически назначаем владельца урока
        """
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели Course с уроками и их количеством"""

    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "lesson_count", "lessons", "owner", "is_subscribed"]

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if not request or not request.user or not request.user.is_authenticated:
            return False
        #  проверяем наличие подписки
        return obj.subscribers.filter(user=request.user).exists()

    def create(self, validated_data):
        """Автоматически назначаем владельца курса"""
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)
