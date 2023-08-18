from rest_framework.generics import ListAPIView

from apps.about.models import Email
from .serializers import EmailSerializer


class EmailListAPIView(ListAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


__all__ = ["EmailListAPIView"]
