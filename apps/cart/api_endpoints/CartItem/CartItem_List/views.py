from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CartItemListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cart = request.session.get(settings.CART_SESSION_ID, None)
        if not cart:
            return Response({'detail': 'The cart is empty yet.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(cart, status=status.HTTP_200_OK)


__all__ = ['CartItemListAPIView']
