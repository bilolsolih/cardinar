from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cart.api_endpoints.CartItem.CartItem_List.serializers import CartItemListSerializer
from apps.cart.models import CartItem


class CartItemDeleteAPIView(DestroyAPIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('device_id', openapi.IN_QUERY, description='Device id', type=openapi.TYPE_STRING),
        ]
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        device_id = self.request.query_params.get('device_id', None)
        if user:
            return CartItem.objects.filter(cart__user=user)
        else:
            return CartItem.objects.filter(device_id=device_id)


class CartItemDeleteAllAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('device_id', openapi.IN_QUERY, description='Device id', type=openapi.TYPE_STRING),])
    def delete(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        device_id = self.request.query_params.get('device_id', None)
        if not user and not device_id:
            raise ValueError('Either user must be authenticated or device_id must be provided')
        return CartItem.objects.filter(Q(cart__user=user) | Q(device_id=device_id))


__all__ = ['CartItemDeleteAPIView', 'CartItemDeleteAllAPIView']
