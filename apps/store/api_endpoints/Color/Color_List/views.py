from rest_framework.generics import ListAPIView

from apps.store.models.product_parameters import Color
from .serializers import ColorListSerializer


class ColorListAPIView(ListAPIView):
    serializer_class = ColorListSerializer
    queryset = Color.objects.all()


__all__ = ['ColorListAPIView']
