from rest_framework.generics import CreateAPIView

from .serializers import InquiryCreateSerializer


class InquiryCreateAPIView(CreateAPIView):
    serializer_class = InquiryCreateSerializer
