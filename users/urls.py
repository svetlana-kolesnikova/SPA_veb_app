from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, UserViewSet

app_name = "users"

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("payments", PaymentViewSet)

urlpatterns = router.urls
