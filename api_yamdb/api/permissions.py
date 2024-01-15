from rest_framework import permissions

from reviews.models import ADMIN, MODERATOR


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.role == ADMIN or request.user.is_superuser))


class IsAuthorAdminModeratorOrReadOnlyPermission(permissions.BasePermission):
    message = (
        'Проверка пользователя является ли он администратором, модератором'
        'или автором объекта, иначе только режим чтения'
    )

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_superuser
                    or request.user.role == ADMIN
                    or request.user.role == MODERATOR
                    or obj.author == request.user))


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.role == ADMIN or request.user.is_superuser
        )
