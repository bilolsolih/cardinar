from rest_framework.generics import RetrieveAPIView

from apps.store.models.product import Polik
from .serializers import PolikRetrieveSerializer


class PolikRetrieveAPIView(RetrieveAPIView):
    serializer_class = PolikRetrieveSerializer
    queryset = Polik.objects.filter(active=True, is_constructed=False)


__all__ = ['PolikRetrieveAPIView']
