from rest_framework.generics import ListAPIView

from apps.about.models import PhoneNumber
from .serializers import PhoneNumberSerializer


class PhoneNumberListView(ListAPIView):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer


__all__ = ["PhoneNumberListView"]
