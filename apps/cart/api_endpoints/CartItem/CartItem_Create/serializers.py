from rest_framework import serializers

from apps.cart.models import CartItem


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['device_id', 'content_type', 'object_id', 'quantity', 'car_model']

    def validate(self, data):
        if hasattr(data, 'device_id') and data['device_id'] and self.context['request'].user.is_authenticated:
            raise serializers.ValidationError('Authenticated users don\'t have to provide device_id.')
        return data

    def create(self, data):
        user = self.context['request'].user
        if user.is_authenticated:
            item = CartItem.objects.create(
                cart=user.cart, content_type=data['product'], object_id=data['object_id'], quantity=data['quantity'], car_model=data['car_model'],
                cost=(data['product'].price * data['quantity'])
            )
        else:
            item = CartItem.objects.create(
                device_id=data['device_id'], content_type=data['product'], object_id=data['object_id'], quantity=data['quantity'],
                car_model=data['car_model'],
                cost=(data['product'].price * data['quantity'])
            )
        return item
