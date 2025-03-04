from rest_framework import permissions


class IsOwnerUser(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только владельцам объекта.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
