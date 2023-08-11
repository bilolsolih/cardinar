from rest_framework.serializers import ModelSerializer

from apps.store.models.product_parameters import Color


class ColorListSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'title', 'hex_value']
