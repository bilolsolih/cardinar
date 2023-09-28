from rest_framework.generics import CreateAPIView

from .serializer import CustomProductCreateSerializer


class CustomProductCreateAPIView(CreateAPIView):
    serializer_class = CustomProductCreateSerializer

    def perform_create(self, serializer):
        model = serializer.save()


__all__ = ['CustomProductCreateAPIView']
