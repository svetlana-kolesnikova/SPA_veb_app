# users/permissions.py
from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Разрешает доступ, если пользователь аутентифицирован и состоит в группе 'Moderators'.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.groups.filter(name="Moderators").exists())


class IsOwner(BasePermission):
    """
    Объектный пермишен: разрешает доступ только владельцу объекта.
    """

    def has_object_permission(self, request, view, obj):
        try:
            return obj.owner == request.user
        except AttributeError:
            # если объект не имеет owner — запретим
            return False


class IsOwnerOrModeratorOrStaff(BasePermission):
    """
    Право для детального просмотра:
    - владелец
    - модератор
    - администратор (superuser)
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        return (
            user == obj              # владелец
            or user.is_staff         # модератор/admin
            or user.is_superuser     # суперпользователь
        )
