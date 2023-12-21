"""Исключения."""
from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            # or request.user.is_staff == True Жду модели пользователей
        )


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    """Доступ к спискам и объектам."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_admin or request.user.is_moderator
                or obj.author == request.user
            )
        )
