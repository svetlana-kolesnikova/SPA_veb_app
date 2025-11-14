# users/permissions.py
from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Разрешает доступ, если пользователь аутентифицирован и состоит в группе 'Moderators'.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.groups.filter(name="Moderators").exists())


class IsNotModerator(BasePermission):
    """
    Разрешает доступ, если пользователь НЕ является модератором.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return not user.groups.filter(name="Moderators").exists()


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
    Объектный пермишен: владелец объекта, модератор или staff(админ) имеют доступ.
    """

    def has_permission(self, request, view):
        # базовая проверка: должен быть аутентифицирован
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True
        if user.groups.filter(name="Moderators").exists():
            # модераторы могут просматривать и редактировать,
            # но контроллеры будут блокировать create/destroy через get_permissions()
            return True
        return getattr(obj, "owner", None) == user
