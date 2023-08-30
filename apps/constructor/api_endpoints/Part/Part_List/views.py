from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from rest_framework.generics import ListAPIView

from apps.constructor.models import Part
from .serializers import PartListSerializer


class PartFilterSet(FilterSet):
    class Meta:
        model = Part
        fields = ['product_model', 'category']


class PartListAPIView(ListAPIView):
    serializer_class = PartListSerializer
    queryset = Part.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartFilterSet


__all__ = ['PartListAPIView']
