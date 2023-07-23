import django_filters
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.store.models.product import Product
from .serializers import ProductListSerializer


class ProductFilterSet(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    target_room = django_filters.ModelMultipleChoiceFilter(field_name='target_room__pk')
    style = django_filters.ModelMultipleChoiceFilter(field_name='style__pk')
    picture_type = django_filters.ModelMultipleChoiceFilter(field_name='picture_type__pk')
    color = django_filters.ModelMultipleChoiceFilter(field_name='color__pk')
    size = django_filters.ModelMultipleChoiceFilter(field_name='size__pk')
    brand = django_filters.ModelMultipleChoiceFilter(field_name='brand__pk')


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.filter(active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilterSet


__all__ = ['ProductListAPIView']
