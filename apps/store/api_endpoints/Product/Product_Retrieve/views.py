from rest_framework.generics import RetrieveAPIView

from apps.store.models.product import Product
from .serializers import ProductRetrieveSerializer


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductRetrieveSerializer
    queryset = Product.objects.filter(active=True)


__all__ = ['ProductRetrieveAPIView']
