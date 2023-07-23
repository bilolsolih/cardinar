from rest_framework.serializers import ModelSerializer

from apps.orders.models import OrderItem


class OrderItemListSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'cost']
        depth = 1
