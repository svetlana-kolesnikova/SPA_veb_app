from rest_framework import serializers

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели Lesson"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели Course с уроками и их количеством"""

    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "lesson_count", "lessons"]

    def get_lesson_count(self, obj):
        return obj.lessons.count()
