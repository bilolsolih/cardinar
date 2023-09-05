from rest_framework.generics import CreateAPIView

from .serializers import ProductCreateSerializer


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductCreateSerializer


__all__ = ['ProductCreateAPIView']
