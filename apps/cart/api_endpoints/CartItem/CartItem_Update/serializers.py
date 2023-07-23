from rest_framework import serializers

from apps.cart.models import CartItem


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
