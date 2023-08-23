from rest_framework.serializers import ModelSerializer

from apps.store.models.product import Product


class ProductRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'main_color',
            'title',
            'type',
            'status',
            'photo',
            'description',
            'price',
            'car_brands',
            'car_models',
            'building_material',
            'created'
        ]
        depth = 1
