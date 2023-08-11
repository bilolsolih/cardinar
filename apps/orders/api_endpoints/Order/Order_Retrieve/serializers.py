from rest_framework import serializers

from apps.orders.models import Order


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'full_name', 'phone_number', 'email', 'delivery_type', 'payment_method', 'final_price', 'created', 'status', 'items'
        ]
        depth = 1
