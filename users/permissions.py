from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем аккаунта"""

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False


class IsSuperuserOrStaff(permissions.BasePermission):
    """Проверка, является ли пользователь суперпользователем или персоналом обслуживания"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.is_staff
