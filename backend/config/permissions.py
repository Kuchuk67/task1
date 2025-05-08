from rest_framework.permissions import BasePermission


class OwnerPermissionsClass(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.pk == request.user.pk:
            return True
        return False
