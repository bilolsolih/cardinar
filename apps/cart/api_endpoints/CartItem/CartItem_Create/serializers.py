from rest_framework import serializers
from django.db import transaction
from apps.cart.models import CartItem


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['device_id', 'product', 'quantity', 'car_model']

    def validate(self, data):
        user = self.context['request'].user
        if hasattr(data, 'device_id') and data['device_id'] and user.is_authenticated:
            raise serializers.ValidationError('Authenticated users don\'t have to provide device_id.')

        if 'device_id' in data and data['device_id']:
            if CartItem.objects.filter(device_id=data['device_id'], product=data['product']).exists():
                raise serializers.ValidationError({'product': 'Item already in the cart.'})
        if user.is_authenticated:
            if CartItem.objects.filter(cart=user.cart, product=data['product']).exists():
                raise serializers.ValidationError({'product': 'Item already in the cart.'})
        return data

    def create(self, data):
        user = self.context['request'].user
        if user.is_authenticated:
            item = CartItem.objects.create(
                cart=user.cart, product=data['product'], quantity=data['quantity'], car_model=data['car_model'],
                cost=(data['product'].price * data['quantity'])
            )
        else:
            item = CartItem.objects.create(
                device_id=data['device_id'], product=data['product'], quantity=data['quantity'], car_model=data['car_model'],
                cost=(data['product'].price * data['quantity'])
            )
        return item
