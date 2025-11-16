# users/views.py
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Payment
from .permissions import IsOwner, IsModerator, IsOwnerOrModeratorOrStaff
from .serializers import PaymentSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    """
    Регистрация нового пользователя — доступна всем (AllowAny).
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для пользователей.
    - list/retrieve/update/partial_update/delete доступны только авторизованным.
    - редактировать свой профиль может только владелец (см. get_permissions below).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated, IsModerator]  # только модеры могут видеть список
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsOwnerOrModeratorOrStaff]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:
            permission_classes = [IsAuthenticated]

        return [perm() for perm in permission_classes]


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для платежей с фильтрацией и сортировкой.
    Доступ: только авторизованные пользователи.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method", "user"]
    ordering_fields = ["payment_date", "amount"]
    ordering = ["-payment_date"]

    def get_permissions(self):
        # все операции над платежами — для авторизованных (в проекте не указано иное)
        return [IsAuthenticated()]
