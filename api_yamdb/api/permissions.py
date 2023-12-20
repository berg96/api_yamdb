from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            # or request.user.status == 'admin' Жду модели пользователей
        )
