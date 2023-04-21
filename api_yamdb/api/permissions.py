from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка роли администратора."""
    message = 'Необходимы права администратора'

    def has_permission(self, request, view):

        user = request.user
        return user.is_authenticated and user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка прав администратора."""
    message = 'Необходимы права администратора'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )


class IsAdminOrModerOrAuthor(permissions.BasePermission):
    """Проверка прав администратора, модератора или админа"""
    message = 'Нет нужных прав, необходимо быть автором, админом, модератором'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moder
            or request.user == obj.author
        )
