# users/views.py
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson

from .models import Payment
from .permissions import IsModerator, IsOwner, IsOwnerOrModeratorOrStaff
from .serializers import PaymentSerializer, RegisterSerializer, UserSerializer
from .services import create_stripe_price, create_stripe_product, create_stripe_session, get_stripe_session_status

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
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated, IsModerator]  # только модеры могут видеть список
        elif self.action == "retrieve":
            permission_classes = [IsAuthenticated, IsOwnerOrModeratorOrStaff]
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsOwner, IsModerator]
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

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.groups.filter(name="Moderators").exists():
            return Payment.objects.all()
        return Payment.objects.filter(user=user)

    def get_permissions(self):
        # все операции над платежами — для авторизованных
        return [IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def buy(self, request):
        """Создание платежа и Stripe-сессии"""

        user = request.user
        course_id = request.data.get("course")
        lesson_id = request.data.get("lesson")

        if not course_id and not lesson_id:
            return Response({"error": "Нужно указать course или lesson"}, status=status.HTTP_400_BAD_REQUEST)

        # определяем объект
        obj, name, amount = None, "", 0

        if course_id:
            obj = Course.objects.get(id=course_id)
            name = obj.name
            amount = obj.price  # Stripe принимает цену в минимальных единицах валюты
        else:
            obj = Lesson.objects.get(id=lesson_id)
            name = obj.name
            amount = obj.price  # Stripe принимает цену в минимальных единицах валюты

        # создаём платёж в БД
        payment = Payment.objects.create(
            user=user,
            course=obj if course_id else None,
            lesson=obj if lesson_id else None,
            amount=amount,
            payment_method="stripe",
        )

        # Создаём продукт и цену в Stripe
        product_id = create_stripe_product(name)
        price_id = create_stripe_price(product_id, amount)

        session_id, payment_url = create_stripe_session(
            price_id,
            success_url="https://example.site/success/",
            cancel_url="https://example.site/cancel/",
        )

        # Сохраняем Stripe данные в платеже
        payment.stripe_product_id = product_id
        payment.stripe_price_id = price_id
        payment.stripe_session_id = session_id
        payment.stripe_payment_url = payment_url
        payment.save()

        return Response(
            {
                "payment_id": payment.id,
                "payment_url": payment_url,
                "session_id": session_id,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated], url_path="status/(?P<session_id>[^/]+)"
    )
    def status(self, request, session_id=None):
        """Проверка статуса Stripe Session"""
        data = get_stripe_session_status(session_id)
        return Response(data)
