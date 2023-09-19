from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView

from apps.store.models.product_parameters import CarBrand
from .serializers import CarBrandListSerializer


class CarBrandListAPIView(ListAPIView):
    serializer_class = CarBrandListSerializer
    queryset = CarBrand.objects.all()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY, description='Category id', type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)
        if category_id:
            return CarBrand.objects.filter(products__category__pk=category_id)
        else:
            return CarBrand.objects.all()


__all__ = ['CarBrandListAPIView']
