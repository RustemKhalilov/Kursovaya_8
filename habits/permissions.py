from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            # print("[[[ user IS owner!!!]]]")
            # print(f"{obj.owner.pk} <> {request.user.pk}")
            return True
        # print("[[[ user IS NOT owner!!!]]]")
        # print(f"{obj.owner.pk} <> {request.user.pk}")
        return False