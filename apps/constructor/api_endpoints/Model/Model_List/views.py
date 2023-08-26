from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.constructor.models import CustomProductModel
from .serializers import CustomProductModelListSerializer


class CustomProductModelFilterSet(FilterSet):
    class Meta:
        model = CustomProductModel
        fields = ['category']


class CustomProductModelListAPIView(ListAPIView):
    serializer_class = CustomProductModelListSerializer
    queryset = CustomProductModel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CustomProductModelFilterSet
