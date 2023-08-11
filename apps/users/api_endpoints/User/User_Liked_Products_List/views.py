from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.store.api_endpoints.CarCover.CarCover_List.serializers import CarCoverListSerializer
from apps.store.api_endpoints.Polik.Polik_List.serializers import PolikListSerializer
from apps.store.api_endpoints.Nakidka.Nakidka_List.serializers import NakidkaListSerializer


class UserLikedProductsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class_map = {
        'carcover': CarCoverListSerializer,
        'polik': PolikListSerializer,
        'nakidka': NakidkaListSerializer
    }
    def get_serializer(self, *args, **kwargs):
        pass


    def get_queryset(self):
        return self.request.user.liked_products.all()
