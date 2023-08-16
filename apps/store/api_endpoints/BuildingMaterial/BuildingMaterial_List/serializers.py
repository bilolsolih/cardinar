from rest_framework.serializers import ModelSerializer

from apps.store.models.product_parameters import BuildingMaterial


class BuildingMaterialListSerializer(ModelSerializer):
    class Meta:
        model = BuildingMaterial
        fields = ['id', 'title']
