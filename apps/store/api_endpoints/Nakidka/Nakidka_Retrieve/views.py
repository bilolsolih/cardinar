from rest_framework.generics import RetrieveAPIView

from apps.store.models.product import Nakidka
from .serializers import NakidkaRetrieveSerializer


class NakidkaRetrieveAPIView(RetrieveAPIView):
    serializer_class = NakidkaRetrieveSerializer
    queryset = Nakidka.objects.filter(active=True, is_constructed=False)


__all__ = ['NakidkaRetrieveAPIView']
