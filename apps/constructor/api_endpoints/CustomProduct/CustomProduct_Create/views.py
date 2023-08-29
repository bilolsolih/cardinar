from rest_framework.generics import CreateAPIView

from .serializer import CustomProductCreateSerializer


class CustomProductCreateAPIView(CreateAPIView):
    serializer_class = CustomProductCreateSerializer


__all__ = ['CustomProductCreateAPIView']
