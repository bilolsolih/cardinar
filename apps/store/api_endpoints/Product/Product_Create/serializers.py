from rest_framework.serializers import ModelSerializer

from apps.store.models.product import Product


class ProductCreateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'category', 'title', 'title_ru', 'title_uz', 'type', 'status', 'photo', 'description',
            'description_ru', 'description_ru', 'price', 'car_models', 'main_color', 'building_material'
        ]
