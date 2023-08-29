from rest_framework import permissions

from apps.payment.authentication import ServerUser


class IsAuthenticatedAndServerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user == ServerUser()
