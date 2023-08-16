from rest_framework.generics import ListAPIView

from apps.about.models import Banner
from .serializers import BannerSerializer


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


__all__ = ["BannerListAPIView"]
