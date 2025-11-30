# users/models.py
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Менеджер пользователей без username, авторизация по email
    """

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен иметь is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Модель пользователя
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="City")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Payment(models.Model):
    """
    Модель платежа
    """

    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счёт"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(
        "materials.Course", on_delete=models.SET_NULL, blank=True, null=True, related_name="payments"
    )
    lesson = models.ForeignKey(
        "materials.Lesson", on_delete=models.SET_NULL, blank=True, null=True, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    stripe_product_id = models.CharField(max_length=200, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=200, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=200, blank=True, null=True)
    stripe_payment_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Платёж от {self.user.email} на {self.amount} ₽"


class CourseSubscription(models.Model):
    """
    Подписка пользователя на обновления курса.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    course = models.ForeignKey("materials.Course", on_delete=models.CASCADE, related_name="subscribers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.email} -> {self.course.name}"
