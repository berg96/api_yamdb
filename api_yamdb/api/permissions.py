from rest_framework import permissions


def is_admin_or_superuser(user):
    return user.is_admin() or user.is_staff or user.is_superuser


class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and is_admin_or_superuser(request.user))


class IsAdminSuperuserOrReadOnly(IsAdminOrSuperuser):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or super().has_permission(request, view))


class IsAuthorAdminSuperuserModeratorOrReadOnly(permissions.BasePermission):
    message = (
        'Проверка пользователя является ли он администратором, модератором'
        'или автором объекта, иначе только режим чтения'
    )

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (is_admin_or_superuser(request.user)
                    or request.user.is_moderator()
                    or obj.author == request.user))
