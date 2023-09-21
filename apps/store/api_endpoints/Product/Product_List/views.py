import django_filters
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.store.models.product import Product, Category
from apps.store.models.product_parameters import CarBrand, CarModel
from .serializers import ProductListSerializer


class ProductFilterSet(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    car_brands = django_filters.ModelMultipleChoiceFilter(field_name='car_brands__pk', queryset=CarBrand.objects.all(), to_field_name='pk')
    car_models = django_filters.ModelMultipleChoiceFilter(field_name='articuls__car_model__pk', queryset=CarModel.objects.all(), to_field_name='pk')
    category = django_filters.ModelMultipleChoiceFilter(field_name='category', queryset=Category.objects.all(), to_field_name='pk')

    class Meta:
        model = Product
        fields = ['main_color', 'status']


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.filter(active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilterSet


__all__ = ['ProductListAPIView']
