import django_filters
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.store.models.product import Polik
from .serializers import PolikListSerializer


class PolikFilterSet(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    car_brands = django_filters.ModelMultipleChoiceFilter(field_name='car_brands__pk')
    car_models = django_filters.ModelMultipleChoiceFilter(field_name='car_models__pk')

    # class Meta:
    #     model = Polik
    #     fields = ['category', 'main_color']


class PolikListAPIView(ListAPIView):
    serializer_class = PolikListSerializer
    queryset = Polik.objects.filter(active=True, is_constructed=False)
    filter_backends = [DjangoFilterBackend]
    filterset_class = PolikFilterSet


__all__ = ['PolikListAPIView']
