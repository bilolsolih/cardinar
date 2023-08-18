from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.store.api_endpoints.Product.Product_List.serializers import ProductListSerializer


class UserLikedProductsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return self.request.user.liked_products.all()
