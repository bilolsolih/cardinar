from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.db import transaction
from django.utils.decorators import method_decorator

from apps.payment.api_endpoints.order.VideoLessonOrderCreate.serializers import (
    VideoLessonOrderCreateSerializer,
)
from apps.payment.models import Order, OrderType


@method_decorator(transaction.non_atomic_requests, name="dispatch")
class VideoLessonOrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = VideoLessonOrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, type=OrderType.VIDEO_LESSON)


__all__ = ["VideoLessonOrderCreateAPIView"]
