from django.db.models.aggregates import Sum
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import OrderItem
from .serializers import OrderCreateSerializer


class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        final_price = user.cart.items.aggregate(final_price=Sum('cost'))['final_price']
        order = serializer.save(user=user, final_price=final_price)
        for item in user.cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, cost=item.cost)
            item.delete()


__all__ = ['OrderCreateAPIView']
