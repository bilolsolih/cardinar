from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView

from apps.store.models.product_parameters import CarBrand
from .serializers import CarBrandListSerializer


class CarBrandListAPIView(ListAPIView):
    serializer_class = CarBrandListSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY, description='Category id', type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id', None)
        print(category_id)
        if category_id:
            return CarBrand.objects.filter(Q(products__category_id=category_id) | Q(cars__products__category_id=category_id))
        else:
            return CarBrand.objects.all()


__all__ = ['CarBrandListAPIView']
