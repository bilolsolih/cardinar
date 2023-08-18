from rest_framework.generics import ListAPIView

from apps.store.models.product_parameters import CarModel
from .serializers import CarModelListSerializer


class CarModelListAPIView(ListAPIView):
    serializer_class = CarModelListSerializer
    lookup_field = "brand_id"

    def get_queryset(self):
        return CarModel.objects.filter(brand__pk=self.kwargs.get('brand_id', None))


__all__ = ['CarModelListAPIView']
