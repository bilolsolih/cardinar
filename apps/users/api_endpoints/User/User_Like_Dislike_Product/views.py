from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.store.models.product import Product


class UserLikeProductAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id, *args, **kwargs):
        user = request.user
        try:
            product = Product.objects.get(active=True, pk=product_id)
            if product not in user.liked_products.all():
                user.liked_products.add(product)
                message = 'Liked'
            else:
                user.liked_products.remove(product)
                message = 'Disliked'
        except Product.DoesNotExist:
            message = 'No such product'
        return Response({'detail': message}, status=status.HTTP_200_OK)


__all__ = ['UserLikeProductAPIView']
