from rest_framework.permissions import BasePermission


class IsNotRegisteredAlready(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous
