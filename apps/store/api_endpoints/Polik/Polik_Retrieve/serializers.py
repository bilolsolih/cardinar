from rest_framework.serializers import ModelSerializer

from apps.store.models.product import Polik


class PolikRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Polik
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
