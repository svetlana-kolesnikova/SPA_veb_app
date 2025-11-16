# users/serializers.py
from rest_framework import serializers

from .models import CourseSubscription, Payment, User


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    password = serializers.CharField(write_only=True, required=True, min_length=5)

    class Meta:
        model = User
        fields = ("email", "password", "phone", "city")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone=validated_data.get("phone"),
            city=validated_data.get("city"),
        )
        return user


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежей"""

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["payment_date"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or hasattr(user, "is_moderator") and user.is_moderator:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя с историей платежей"""

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "city", "avatar", "payments"]
        read_only_fields = ["id", "payments"]

    def to_representation(self, instance):
        request = self.context.get("request", None)
        rep = super().to_representation(instance)
        if request is None:
            return rep
        # если запрошенный профиль — не текущий пользователь, прячем платежи и lastname
        if request.user.is_authenticated and request.user != instance:
            rep.pop("payments", None)
            rep.pop("last_name", None)
        return rep


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки"""

    class Meta:
        model = CourseSubscription
        fields = ["id", "user", "course", "created_at"]
        read_only_fields = ["id", "created_at", "user"]
