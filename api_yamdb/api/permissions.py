from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def is_admin(self, user):
        return user.is_admin()

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and self.is_admin(request.user))


class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or super().has_permission(request, view))


class IsAuthorAdminModeratorOrReadOnly(IsAdmin):
    message = (
        'Проверка пользователя является ли он администратором, модератором'
        'или автором объекта, иначе только режим чтения'
    )

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (super().is_admin(request.user)
                    or request.user.is_moderator()
                    or obj.author == request.user))
