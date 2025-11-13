from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с моделью User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления платежами.
    Реализует фильтрацию по курсу, уроку и способу оплаты, а также сортировку по дате оплаты.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]  # по умолчанию — последние платежи первыми
