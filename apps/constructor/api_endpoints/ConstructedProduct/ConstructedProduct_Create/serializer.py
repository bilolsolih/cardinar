from rest_framework import serializers

from apps.constructor.models import ConstructedProduct


class ConstructedProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructedProduct
        fields = ['category', 'building_material',]
