from rest_framework import permissions


class AnonimOrAuthenticatedReadOnly(permissions.BasePermission):
    """ Доступ для анонимных и авторизованных пользователей
    только к безопасным методам и POST-запросам для регистрации. """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True  # Разрешаем POST-запросы всем
        return (
            (request.method in permissions.SAFE_METHODS
             and (request.user.is_anonymous
                  or request.user.is_authenticated))
            or request.user.is_superuser
            or request.user.is_staff
        )


class AuthorOrReadOnly(permissions.BasePermission):
    """ Доступ только для авторов объектов, остальные методы запрещены. """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
