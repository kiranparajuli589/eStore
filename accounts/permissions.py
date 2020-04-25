from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Allow access only to admin users
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)
