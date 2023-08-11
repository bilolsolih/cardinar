from django.contrib.auth import logout
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated


class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        logout(self.request)


__all__ = ['UserDeleteAPIView']
