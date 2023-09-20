from rest_framework.serializers import ModelSerializer

from apps.store.models.product import Product, Articul
from apps.store.models.product_parameters import CarModel


class CarModelInArticul(ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'


class ArticulInProduct(ModelSerializer):
    car_model = CarModelInArticul(many=False)

    class Meta:
        model = Articul
        fields = '__all__'


class ProductRetrieveSerializer(ModelSerializer):
    articuls = ArticulInProduct(many=True)

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
            'photos',
            'description',
            'price',
            'car_brands',
            'articuls',
            'building_material',
            'images',
            'created'
        ]
        depth = 1
