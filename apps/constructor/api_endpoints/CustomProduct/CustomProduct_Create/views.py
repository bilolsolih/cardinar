from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser

from .serializer import CustomProductCreateSerializer


class CustomProductCreateAPIView(CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = CustomProductCreateSerializer

    def perform_create(self, serializer):
        model = serializer.save()


__all__ = ['CustomProductCreateAPIView']
