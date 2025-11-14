# users/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import PaymentViewSet, RegisterAPIView, UserViewSet

app_name = "users"

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("payments", PaymentViewSet, basename="payment")


urlpatterns = [
    path("", include(router.urls)),
    # Регистрация
    path("register/", RegisterAPIView.as_view(), name="register"),
    # JWT авторизация
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
