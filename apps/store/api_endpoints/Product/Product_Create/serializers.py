from rest_framework.serializers import ModelSerializer

from apps.store.models.product import Product


class ProductCreateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'title', 'type', 'status', 'photo', 'description', 'price', 'car_models', 'main_color', 'building_material']
