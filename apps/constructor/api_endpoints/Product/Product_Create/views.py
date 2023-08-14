from rest_framework.generics import CreateAPIView

from .serializer import ProductCreateSerializer


class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductCreateSerializer

    def perform_create(self, serializer):
        serializer.save(is_constructed=True)


__all__ = ['ProductCreateAPIView']
