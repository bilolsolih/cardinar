from rest_framework.generics import CreateAPIView

from .serializer import ConstructedProductCreateSerializer


class ConstructedProductCreateAPIView(CreateAPIView):
    serializer_class = ConstructedProductCreateSerializer

    def perform_create(self, serializer):
        serializer.save(is_constructed=True)


__all__ = ['ConstructedProductCreateAPIView']
