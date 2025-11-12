from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """ViewSet для работы с моделью Course."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Представление для получения списка уроков и создания нового урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, изменения и удаления конкретного урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
