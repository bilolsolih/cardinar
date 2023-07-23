from rest_framework.generics import ListAPIView

from apps.store.models.product_parameters import BuildingMaterial
from .serializers import BuildingMaterialListSerializer


class BuildingMaterialListAPIView(ListAPIView):
    serializer_class = BuildingMaterialListSerializer
    queryset = BuildingMaterial.objects.all()


__all__ = ['BuildingMaterialListAPIView']
