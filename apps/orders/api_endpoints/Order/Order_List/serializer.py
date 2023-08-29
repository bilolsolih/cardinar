from rest_framework import serializers

from apps.orders.models import Order


class OrderListSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    def get_quantity(self, instance):
        return instance.items.count()

    class Meta:
        model = Order
        fields = ['id', 'created', 'quantity', 'final_price', 'status', 'payment_status']
