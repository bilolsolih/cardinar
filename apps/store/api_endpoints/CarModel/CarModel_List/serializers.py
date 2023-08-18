from rest_framework.serializers import ModelSerializer

from apps.store.models.product_parameters import CarModel


class CarModelListSerializer(ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'title', 'brand']
