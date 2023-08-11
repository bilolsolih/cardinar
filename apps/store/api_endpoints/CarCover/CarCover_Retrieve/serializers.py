from rest_framework.serializers import ModelSerializer

from apps.store.models.product import CarCover


class CarCoverRetrieveSerializer(ModelSerializer):
    class Meta:
        model = CarCover
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
            'created',
            'central_part_color',
            'central_part_material',
            'rear_color',
            'rear_material',
            'side_color',
            'side_material',
            'stitch_color',
            'has_kant',
            'kant_color'
        ]
        depth = 1
