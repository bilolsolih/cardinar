from rest_framework.generics import ListAPIView
from apps.about.models import Address
from .serializers import AddressSerializer


class AddressListAPIView(ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


__all__ = ["AddressListAPIView"]
