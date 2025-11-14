# materials/serializers.py
from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели Lesson"""

    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "preview", "video_link", "course", "owner"]

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

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "lesson_count", "lessons", "owner"]

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def create(self, validated_data):
        """
        Автоматически назначаем владельца курса
        """
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)
