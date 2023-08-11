from django.conf import settings
from django.apps import apps
from rest_framework.generics import CreateAPIView

from .serializers import CartItemCreateSerializer


class CartItemCreateUpdateAPIView(CreateAPIView):
    serializer_class = CartItemCreateSerializer

    def perform_create(self, serializer):
        cart = self.request.session.get(settings.CART_SESSION_ID, None)
        if not cart:
            cart = self.request.session[settings.CART_SESSION_ID] = {}
        data = serializer.validated_data
        cart[id] = {
            'content_type': data['content_type'],
            'id': data['product_id'],
            'title': data['title'],
            'quantity': data['quantity'],
            'photo': self.request.build_absolute_uri(data['url']),
            'cost': data['price'] * data['quantity']
        }
        self.request.session.modified = True


__all__ = ['CartItemCreateUpdateAPIView']
