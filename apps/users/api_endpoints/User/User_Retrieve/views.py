from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserRetrieveSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


__all__ = ['UserRetrieveAPIView']
