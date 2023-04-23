from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка роли администратора."""
    def has_permission(self, request, view):

        user = request.user
        return user.is_authenticated and user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права доступа для проверки, является ли пользователь администратором.
    Если пользователь не является администратором,
    то ему разрешены только безопасные запросы (GET, HEAD, OPTIONS).
    """

    message = 'Необходимы права администратора'

    def has_permission(self, request, view):
        """Проверка наличия прав у пользователя на выполнение запроса."""
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
