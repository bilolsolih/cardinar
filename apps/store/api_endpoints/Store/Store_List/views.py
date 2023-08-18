from rest_framework.generics import ListAPIView

from apps.store.models.store import Store
from .serializers import StoreListSerializer


class StoreListAPIView(ListAPIView):
    serializer_class = StoreListSerializer
    queryset = Store.objects.all()


__all__ = ['StoreListAPIView']
