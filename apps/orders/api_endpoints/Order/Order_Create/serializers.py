from rest_framework import serializers

from apps.orders.models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'email', 'store', 'delivery_type']

    def validate(self, attrs):
        request = self.context['request']
        user = request.user if request.user.is_authenticated else None
        device_id = request.query_params.get('device_id', None)
        if user and device_id:
            raise serializers.ValidationError('device_id is needed for guest users only.')
        if not user and not device_id:
            raise serializers.ValidationError('Either user must be authenticated or device_id must be provided.')
        return attrs
