from rest_framework import permissions


class AnonimOrAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return (
            (request.method in permissions.SAFE_METHODS
             and (request.user.is_anonymous
                  or request.user.is_authenticated))
            or request.user.is_superuser
            or request.user.is_staff
        )
