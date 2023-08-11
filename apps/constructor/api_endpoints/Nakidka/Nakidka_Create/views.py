from rest_framework.generics import CreateAPIView

from apps.store.models.product import Polik
from .serializer import NakidkaCreateSerializer


class NakidkaCreateAPIView(CreateAPIView):
    serializer_class = NakidkaCreateSerializer

    def perform_create(self, serializer):
        serializer.save(is_constructed=True)


__all__ = ["NakidkaCreateAPIView"]
