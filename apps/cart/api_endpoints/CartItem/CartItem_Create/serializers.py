from rest_framework import serializers

from apps.cart.models import CartItem


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['device_id', 'product', 'articul', 'quantity', 'car_model']

    def create(self, data):
        cart = self.context['request'].user.cart if self.context['request'].user.is_authenticated else None
        item = CartItem.objects.create(cart=cart, **data)

        return item

    def validate(self, data):
        user = self.context['request'].user
        if not user.is_authenticated and 'device_id' not in data and not data['device_id']:
            raise serializers.ValidationError('Either user must be authenticated or device_id must be provided.')

        if 'device_id' in data and data['device_id']:
            if CartItem.objects.filter(device_id=data['device_id'], articul=data['articul']).exists():
                raise serializers.ValidationError({'product': 'Item already in the cart.'})

        if user.is_authenticated:
            if CartItem.objects.filter(cart=user.cart, articul=data['articul']).exists():
                raise serializers.ValidationError({'product': 'Item already in the cart.'})

        data['cost'] = data['product'].price * data['quantity']

        return data
