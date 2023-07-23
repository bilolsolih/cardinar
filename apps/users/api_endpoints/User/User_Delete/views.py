from django.contrib.auth import logout
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.models import User


class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instanc.cart.delete()
        instance.save()
        logout(self.request)


__all__ = ['UserDeleteAPIView']
