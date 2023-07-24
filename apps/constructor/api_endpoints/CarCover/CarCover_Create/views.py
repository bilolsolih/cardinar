from rest_framework.generics import CreateAPIView

from .serializer import CarCoverCreateSerializer
from apps.store.models.product import CarCover


class CarCoverCreateAPIView(CreateAPIView):
    queryset = CarCover.objects.all()
    serializer_class = CarCoverCreateSerializer

    def perform_create(self, serializer):
        serializer.save(is_constructed=True)


__all__ = ['CarCoverCreateAPIView']
