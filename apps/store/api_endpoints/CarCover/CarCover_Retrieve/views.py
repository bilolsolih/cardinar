from rest_framework.generics import RetrieveAPIView

from apps.store.models.product import CarCover
from .serializers import CarCoverRetrieveSerializer


class CarCoverRetrieveAPIView(RetrieveAPIView):
    serializer_class = CarCoverRetrieveSerializer
    queryset = CarCover.objects.filter(active=True, is_constructed=False)


__all__ = ['CarCoverRetrieveAPIView']
