from rest_framework.generics import ListAPIView

from apps.store.models.product_parameters import CarBrand
from .serializers import CarBrandListSerializer


class CarBrandListAPIView(ListAPIView):
    serializer_class = CarBrandListSerializer
    queryset = CarBrand.objects.all()


__all__ = ['CarBrandListAPIView']
