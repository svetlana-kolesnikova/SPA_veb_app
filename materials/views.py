# materials/views.py
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import CourseSubscription
from users.permissions import IsOwner, IsOwnerOrModeratorOrStaff
from users.serializers import CourseSubscriptionSerializer

from .models import Course, Lesson
from .paginators import StandardResultsSetPagination
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """ViewSet для работы с моделью Course."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOwnerOrModeratorOrStaff]
        else:  # list, retrieve
            permission_classes = [IsAuthenticated]

        return [perm() for perm in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        """Подписаться на курс"""
        course = self.get_object()
        user = request.user
        sub, created = CourseSubscription.objects.get_or_create(user=user, course=course)
        if not created:
            return Response({"detail": "Уже подписан."}, status=status.HTTP_200_OK)
        return Response(
            CourseSubscriptionSerializer(sub, context={"request": request}).data, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated], url_path="unsubscribe")
    def unsubscribe(self, request, pk=None):
        """Отписаться от курса"""
        course = self.get_object()
        user = request.user
        qs = CourseSubscription.objects.filter(user=user, course=course)
        deleted, _ = qs.delete()
        if deleted:
            return Response({"detail": "Отписка выполнена."}, status=status.HTTP_200_OK)
        return Response({"detail": "Подписка не найдена."}, status=status.HTTP_404_NOT_FOUND)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Представление для получения списка уроков и создания нового урока"""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [perm() for perm in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Представление для получения, изменения и удаления конкретного урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            permission_classes = [IsAuthenticated, IsOwnerOrModeratorOrStaff]
        elif self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [perm() for perm in permission_classes]
