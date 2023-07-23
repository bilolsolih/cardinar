from rest_framework.serializers import ModelSerializer

from apps.orders.models import Order


class OrderCreateSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'email', 'store', 'delivery_type', 'payment_method']
