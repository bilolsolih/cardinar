from rest_framework.serializers import ModelSerializer

from apps.store.models.product_parameters import CarBrand


class CarBrandListSerializer(ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ['id', 'title']
