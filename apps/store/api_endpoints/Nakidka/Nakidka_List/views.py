import django_filters
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.store.models.product import Nakidka
from .serializers import NakidkaListSerializer


class NakidkaFilterSet(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    car_brands = django_filters.ModelMultipleChoiceFilter(field_name='car_brands__pk')
    car_models = django_filters.ModelMultipleChoiceFilter(field_name='car_models__pk')

    class Meta:
        model = Nakidka
        fields = ['category', 'main_color']


class NakidkaListAPIView(ListAPIView):
    serializer_class = NakidkaListSerializer
    queryset = Nakidka.objects.filter(active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = NakidkaFilterSet


__all__ = ['NakidkaListAPIView']
