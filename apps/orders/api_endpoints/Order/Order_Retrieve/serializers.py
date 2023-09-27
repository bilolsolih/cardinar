from rest_framework import serializers

from apps.orders.models import Order


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'get_title', 'full_name', 'phone_number', 'email', 'delivery_type', 'final_price', 'created', 'status', 'payment_status', 'items', 'city', 'region', 'address', 'level', 'delivery_date'
        ]
        depth = 1
