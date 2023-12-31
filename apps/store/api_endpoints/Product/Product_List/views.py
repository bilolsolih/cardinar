import django_filters
from django.db.models import Q
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.store.models.product import Product, Category
from apps.store.models.product_parameters import CarBrand, CarModel
from .serializers import ProductListSerializer


class ProductFilterSet(FilterSet):
    car_brands = django_filters.ModelMultipleChoiceFilter(field_name='car_brands__pk', queryset=CarBrand.objects.all(), to_field_name='pk')
    car_models = django_filters.ModelMultipleChoiceFilter(field_name='articuls__car_model__pk', queryset=CarModel.objects.all(), to_field_name='pk')
    category = django_filters.ModelMultipleChoiceFilter(field_name='category', queryset=Category.objects.all(), to_field_name='pk')
    price__min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['main_color', 'status']


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilterSet

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        s = self.request.query_params.get('s', None)
        if s:
            queryset = queryset.filter(Q(title__icontains=s) | Q(articuls__car_model__title__icontains=s)).distinct()
        return queryset


__all__ = ['ProductListAPIView']
