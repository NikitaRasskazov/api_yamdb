from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Проверка роли администратора."""
    def has_permission(self, request, view):

        user = request.user
        return user.is_authenticated and user.is_admin
