from rest_framework.generics import ListAPIView

from apps.about.models import SocialMedia
from .serializers import SocialMediaSerializer


class SocialMediaListAPIView(ListAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer


__all__ = ["SocialMediaListAPIView"]
