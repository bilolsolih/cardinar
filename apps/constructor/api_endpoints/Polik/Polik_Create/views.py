from rest_framework.generics import CreateAPIView

from apps.store.models.product import Polik
from .serializer import PolikCreateSerializer


class PolikCreateAPIView(CreateAPIView):
    queryset = Polik.objects.all()
    serializer_class = PolikCreateSerializer

    def perform_create(self, serializer):
        serializer.save(is_constructed=True)


__all__ = ['PolikCreateAPIView']
