from django_filters.rest_framework.backends import DjangoFilterBackend
from django_filters.rest_framework.filterset import FilterSet
from rest_framework.generics import ListAPIView

from apps.store.models.product_parameters import CarBrand
from .serializers import CarBrandListSerializer


class CarBrandFilterSet(FilterSet):
    class Meta:
        model = CarBrand
        fields = ['products__category']


class CarBrandListAPIView(ListAPIView):
    serializer_class = CarBrandListSerializer
    queryset = CarBrand.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarBrandFilterSet


__all__ = ['CarBrandListAPIView']
