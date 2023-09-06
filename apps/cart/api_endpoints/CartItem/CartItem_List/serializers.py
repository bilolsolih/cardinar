from rest_framework import serializers

from apps.cart.models import CartItem
from apps.store.models.product import Product


class ProductInCartItem(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'photo', 'category']


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductInCartItem(many=False)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'cost']
