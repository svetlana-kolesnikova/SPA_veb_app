from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer

class UserViewSet(ModelViewSet):
    """ViewSet для работы с моделью User"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
