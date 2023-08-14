from rest_framework.generics import ListAPIView

from apps.store.models.product_parameters import CarModel
from .serializers import CarModelListSerializer


class CarModelListAPIView(ListAPIView):
    serializer_class = CarModelListSerializer
    queryset = CarModel.objects.all()


__all__ = ['CarModelListAPIView']
