import django_filters
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.store.models.product import CarCover
from .serializers import CarCoverListSerializer


class CarCoverFilterSet(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    car_brands = django_filters.ModelMultipleChoiceFilter(field_name='car_brands__pk')
    car_models = django_filters.ModelMultipleChoiceFilter(field_name='car_models__pk')

    class Meta:
        model = CarCover
        fields = ['category', 'main_color']


class CarCoverListAPIView(ListAPIView):
    serializer_class = CarCoverListSerializer
    queryset = CarCover.objects.filter(active=True, is_constructed=False)
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarCoverFilterSet


__all__ = ['CarCoverListAPIView']
